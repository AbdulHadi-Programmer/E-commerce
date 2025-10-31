### 31 October 2025: 
### Level 1: Basic Image Upload (Single File)
Goal
Upload a single image with an API (e.g, profile picture or book cover)

### Step 1: Model Setup 
Let's create a simple model called Profile in a new app called uploads (or your lab app)
```py
# models.py
```
**🧠 Explanation:**
- upload_to='profile_images/' → images will be stored inside /media/profile_images/.
- blank=True, null=True → allows creating a profile without an image first.

### Step 2: Settings Configuration 
Open settings.py and add this near the bottom 

```py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
Then in your own `urls.py`:
```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your routes ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# This allows Django to serve uploaded files in development mode. 
```

### Step 3: Serializer 
```py
# lab/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'image']
        read_only_fields = ['user']
```
### Step 4: APIView 
```py
# lab/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

class ProfileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
```

### Step 5: URLs
```py
# lab/urls.py
from django.urls import path
from .views import ProfileUploadView

urlpatterns = [
    path('profile/', ProfileUploadView.as_view(), name='profile-upload'),
]
```

### Step 6: Testing in Postman 
POST request → http://127.0.0.1:8000/lab/profile/

**Body (form-data):**
| Key   | Type | Value               |
| ----- | ---- | ------------------- |
| bio   | Text | "Backend Developer" |
| image | File | (select an image)   |

## Output Example:
```json
{
  "id": 1,
  "user": 1,
  "bio": "Backend Developer",
  "image": "http://127.0.0.1:8000/media/profile_images/avatar.jpg"
}
```

### How It Works:  
- DRF automatically handles multipart/form-data uploads where the Content-Type header is set.
- Django stores the image in MEDIA_ROOT/profile_images/.
- Serializer's ImageField automatically returns the absolute file path in the API response.

<!-- ## Level 2 : Multiple File Uploads (like uploading 5 images for a product) -->

## ⚙️ LEVEL 2 — Multiple File Uploads (Real-World Product Images Example)
🎯 Goal

✅ Step 1: Models
```py
# media_lab/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid
import os

User = get_user_model()


# Utility function to rename uploaded files uniquely
def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"  # Rename file to UUID
    return os.path.join('uploads/', filename)


# ---------- LEVEL 2: Multiple Upload Example ----------
class Album(models.Model):
    """A collection of photos uploaded by a user"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Album: {self.name}"


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo in {self.album.name}"
# ✅ Why this model?
# - Album is like a container (a user can create multiple albums).
# - Each album has many photos → great to learn multi-upload and validations cleanly.
```
## Level 2 — Multiple File Uploads (APIView Only)
🔸 Serializer

