from .models import *
from .serializers import *

from rest_framework import viewsets, permissions
from rest_framework.decorators import action

class PostApiList(viewsets.ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Yangi post obyektini avtor sifatida saqlash.
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Berilgan postga foydalanuvchi tomonidan like qo'shish.
        Agar foydalanuvchi allaqachon like qo'shgan bo'lsa, uni o'chirish.
        """
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()


class CommentApiList(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Berilgan postga tegishli kommentarilarni qaytarish.
        """
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """
        Yangi kommentar obyektini avtor sifatida saqlash.
        """
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(id=post_id, published=True)
        serializer.save(user=self.request.user, post=post)


class LikeApiList(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def toggle_like(self, request, pk=None):
        """
        Berilgan post uchun foydalanuvchi tomonidan like ni o'chirish yoki qo'shish.
        Agar foydalanuvchi allaqachon like qo'shgan bo'lsa, uni o'chirish.
        """
        post = Post.objects.get(id=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()
