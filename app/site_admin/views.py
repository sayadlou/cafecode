from django.shortcuts import render
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from .forms import *
from .serializers import *

menus = [

    {
        "app_name": "account",
        "model": Customer,
        "label": "Customer Management",
        "icon": "fa-chart-pie",
        "view_serializer": CustomerSerializerView,
        "all_serializer": CustomerSerializerAll,
        "add_form": CreateCustomerForm,
        "signup_form": CreateUserForm,

    },
    {
        "app_name": "contact_us",
        "model": Contact,
        "label": "Message Management",
        "icon": "fa-envelope",
        "view_serializer": ContactSerializerView,
        "all_serializer": ContactSerializerAll,
        "add_form": ContactForm,
    },
    {
        "app_name": "blog",
        "model": Post,
        "label": "Post Management",
        "icon": "fa-book",
        "view_serializer": PostSerializerAll,
        "all_serializer": PostSerializerView,
        "add_form": PostForm,
    },
    {
        "app_name": "blog",
        "model": Category,
        "label": "Category Management",
        "icon": "fa-tags",
        "view_serializer": CategorySerializerAll,
        "all_serializer": CategorySerializerView,
        "add_form": CategoryForm,
    },
    {
        "app_name": "blog",
        "model": Comment,
        "label": "Comment Management",
        "icon": "fa-comments",
        "view_serializer": CommentSerializerAll,
        "all_serializer": CommentSerializerView,
        "add_form": CommentForm,
    },
    {
        "app_name": "product",
        "model": Product,
        "label": "Product Management",
        "icon": "fa-coffee",
        "view_serializer": ProductSerializerAll,
        "all_serializer": ProductSerializerView,
        "add_form": ProductForm,
    },
    {
        "app_name": "product",
        "model": Extension,
        "label": "Extension Management",
        "icon": "fa-plus",
        "view_serializer": ExtensionSerializerAll,
        "all_serializer": ExtensionSerializerView,
        "add_form": ExtensionForm,
    },
]


def dashboard(request, tk=1, cat="list", item=0):
    menu_list = []
    no_data = False
    for menu in menus:
        menu_list.append(dict(label=menu["label"], icon=menu["icon"]))
    if int(tk) <= len(menus) and int(tk) != 0:
        model = int(tk) - 1
    else:
        raise Http404("Model not found")
    if request.method == 'POST':
        if cat == "add":
            if model == 0:
                form = CreateUserForm(request.POST)
                form2 = CreateCustomerForm(request.POST, request.FILES)
                if form.is_valid():
                    user = form.save()
                    customer = Customer.objects.create(user=user)
                    form2 = CreateCustomerForm(request.POST, request.FILES, instance=customer)
                    if form2.is_valid():
                        messages.success(request, "customer created")
                        return HttpResponseRedirect(reverse('dashboard', args=(tk, "list", '0')))
                    else:
                        user.delete()
                        context = {
                            "page_type": "add",
                            "menu_list": menu_list,
                            "form": form2,
                            'signup_form': form,
                            "model": str(tk),
                        }
                        return render(request, 'site_admin/dashboard.html', context)
                else:
                    context = {
                        "page_type": "add",
                        "menu_list": menu_list,
                        "form": form2,
                        'signup_form': form,
                        "model": str(tk),
                    }
                    return render(request, 'site_admin/dashboard.html', context)
            else:
                form = menus[model]["add_form"](request.POST, request.FILES)
                if form.is_valid():
                    form.save()
                    messages.info(request, "Added successfully")
                    return HttpResponseRedirect(reverse('dashboard', args=(tk, "list", '0')))
                else:
                    context = {
                        "page_type": "add",
                        "menu_list": menu_list,
                        "form": form,
                        "model": str(tk)
                    }
                    messages.error(request, "Adding feild")
                    return render(request, 'site_admin/dashboard.html', context)
        elif cat == "edit":
            Model = menus[model]["model"]
            obj = Model.view_it(Model, item)
            form = menus[model]["add_form"](request.POST, instance=obj)
            if form.is_valid():
                form.save()
                messages.info(request, "Edited successfully")
                return HttpResponseRedirect(reverse('dashboard', args=(tk, "list", '0')))
            else:
                context = {
                    "page_type": "add",
                    "menu_list": menu_list,
                    "form": form,
                    "model": str(tk)
                }
                messages.error(request, "Editing field")
                return render(request, 'site_admin/dashboard.html', context)
        else:
            raise Http404("wrong function")
    elif request.method == 'GET':
        if cat == "list":
            # print(User.objects.get(groups__name="admin"))
            Model = menus[model]["model"]
            all_item = Model.objects.all()
            if all_item.count() == 0:
                no_data = True
            table = menus[model]["all_serializer"](all_item, many=True).data
            context = {
                "page_type": "list",
                "menu_list": menu_list,
                "no_data": no_data,
                "table": table,
                "model": str(tk),
                "title": menus[model]["label"],
            }
            return render(request, 'site_admin/dashboard.html', context)
        elif cat == "view":
            Model = menus[model]["model"]
            obj = Model.view_it(Model, item)
            if not obj:
                raise Http404("wrong item")
            table = menus[model]["view_serializer"](obj).data
            context = {
                "page_type": "view",
                "menu_list": menu_list,
                "table": table,
                "model": str(tk),
                "item": item
            }
            return render(request, 'site_admin/dashboard.html', context)
        elif cat == "add":
            form = menus[model]["add_form"]
            signup_form = False
            if model == 0:
                signup_form = menus[model]["signup_form"]
            context = {
                "page_type": "add",
                "menu_list": menu_list,
                "form": form,
                'signup_form': signup_form,
                "model": str(tk),
            }
            return render(request, 'site_admin/dashboard.html', context)
        elif cat == "edit":
            Model = menus[model]["model"]
            obj = Model.view_it(Model, item)
            form = menus[model]["add_form"](instance=obj)
            context = {
                "page_type": "edit",
                "menu_list": menu_list,
                "form": form,
                "model": str(tk)
            }
            return render(request, 'site_admin/dashboard.html', context)
        elif cat == "delete":
            context = {
                "page_type": "delete",
            }
            Model = menus[model]["model"]
            if Model.delete_it(Model, item):
                messages.success(request, "Item deleted")
            else:
                messages.error(request, "Item not found")
            return HttpResponseRedirect(reverse('dashboard', args=(tk, "list", '0')))
        else:
            raise Http404("wrong function")
    else:
        raise Http404("wrong function")
