from .forms import ProductSearchForm


def search_form(request):
    return {"search_form": ProductSearchForm()}
