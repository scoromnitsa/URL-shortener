from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseGone
from .models import ShortURL, ClickStat
from .serializers import ShortURLSerializer
from rest_framework.views import APIView
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        short_code = request.data.get('short_code')
        if short_code:
            if ShortURL.objects.filter(short_code=short_code).exists():
                return Response({"error": "This short code already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        obj = self.get_object()
        obj.is_active = False
        obj.save()
        return Response({"status": "deactivated"})

@api_view(['GET'])
@permission_classes([]) 
def redirect_view(request, short_code):
    obj = get_object_or_404(ShortURL, short_code=short_code)
    if not obj.is_active or obj.is_expired():
        return HttpResponseGone("Link inactive or expired.")
    ClickStat.objects.create(short_url=obj)
    return redirect(obj.orig_link)

class StatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        now = timezone.now()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        data = []
        for url in ShortURL.objects.filter(is_active=True):
            clicks = url.clicks.all()
            last_hour = clicks.filter(timestamp__gte=one_hour_ago).count()
            last_day = clicks.filter(timestamp__gte=one_day_ago).count()

            data.append({
                "link": request.build_absolute_uri(f"/r/{url.short_code}/"),
                "orig_link": url.orig_link,
                "last_hour_clicks": last_hour,
                "last_day_clicks": last_day,
                "total_clicks": clicks.count(),
            })

        data.sort(key=lambda x: x["last_day_clicks"], reverse=True)
        return Response(data)