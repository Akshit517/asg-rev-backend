from django.http import JsonResponse
import json

def asset_links(request):
    asset_links_data =[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target" : { "namespace": "android_app", "package_name": "com.example.asgrev",
               "sha256_cert_fingerprints": ["A6:A3:C4:AC:03:97:D5:45:B8:B1:AD:33:57:04:1B:F0:62:0A:30:4B:20:57:D4:11:17:DF:B6:3E:47:EB:CD:6C"] }
}]
    return JsonResponse(asset_links_data, content_type="application/json", safe=False)
