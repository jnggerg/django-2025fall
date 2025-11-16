from django.shortcuts import redirect
from functools import wraps

# this decorator is used for checking the "auctioneer" privilages, so only the auctioneer can start / close auctions
def group_required(*group_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return redirect('home')
        return _wrapped_view
    return decorator