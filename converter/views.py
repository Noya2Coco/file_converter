from django.shortcuts import get_object_or_404, redirect, render
from django.http import FileResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from converter.models import Conversion

@csrf_exempt  # Nécessaire pour les requêtes AJAX si CSRF est activé
def upload_file_view(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        input_file = request.FILES['input_file']
        source_format = input_file.name.split('.')[-1].lower()
        target_format = request.POST.get('target_format')

        conversion = Conversion.objects.create(
            input_file=input_file,
            source_format=source_format,
            target_format=target_format
        )
            
        try:
            conversion.convert_file()
            if conversion.converted:
                return JsonResponse({
                    "status": "success",
                    "download_url": f"/converter/download/{conversion.token}/",
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": conversion.error_message or "Conversion failed",
                })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Error during conversion: {e}",
            })

    return render(request, 'converter/converter.html')

def convert_file_view(request, conversion_token):
    conversion = get_object_or_404(Conversion, token=conversion_token)
        
    if not conversion.converted:
        print(conversion.error_message)
        return render(request, 'converter/error.html', {
            'error_message': conversion.error_message or "Conversion failed"
        })

    return render(request, 'converter/success.html', {
        'download_url': f"/converter/download/{conversion.token}/"
    })

def download_file_view(request, conversion_token):
    try:
        conversion = get_object_or_404(Conversion, token=conversion_token)
        if not conversion.output_file:
            raise Http404("File not found")
        file_path = conversion.output_file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=conversion.output_file.name)
    except Exception as e:
        raise Http404(f"Error downloading file: {str(e)}")

