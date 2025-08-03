from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out the user before deleting
    user.delete()
    return redirect('home')  # or another landing page
