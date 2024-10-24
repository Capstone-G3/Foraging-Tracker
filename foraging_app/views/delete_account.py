from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,  render
from django.views import View


class DeleteUserView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'delete_form.html')
    
    def post(self, request):
        user = request.user
        # user_objs = User.objects.filter(user.id)
        # user_objs.delete()
        user.delete()
        return redirect('home')
