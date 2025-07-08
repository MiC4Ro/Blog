from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrlib.auth.mixins import LoginReqiredMixin, UserPassesTestMixin
from .models import Post

class PostUpdateView(LoginReqiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/edit_post.html'

    def test_func(self):
        post = self.get_object()
        return post.can_edit(self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs = {'pk': self.object.id})
    
class PostDeleteView(LoginReqiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return post.can_delete(self.request.user)