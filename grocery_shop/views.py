
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required


def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            messages.info(request, "Try again")
    context = {"form": form}
    return render(request, "register.html", context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            email = user.email
            request.session['username']= user.username
            request.session['email'] = user.email
            obj = Owner.objects.filter(email=email).first()
            if obj is not None:
                return redirect("ownerHome")
            else:
                obj = Employee.objects.filter(email=email).first()
                if obj is not None:
                    return redirect("employeeHome")
                else:
                    return redirect("userHome")
        else:
            messages.info(request, "username or password incorrect")
    # print("yor are", request.session.get('email'))
    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("home")

def home(request):
    return render(request, "home.html")


# --------------------------------------------------Customer----------------------------------------------------------


@login_required(login_url="login")
def userHome(request):
    if(request.session.get('email') == None):
        return redirect("login")
    else :
        return render(request, "userHome.html")


def show_items(request, data=None):
    email = request.session.get('email')
    allD = Employee.objects.filter(email=email).first()
    obj = Owner.objects.filter(email=email).first()
    if data == None or data == "All_Products":
        sch = Inventory.objects.filter(quantity__gte=1).all()
        context = {"sch": sch}
    elif data == "Beverage":
        sch = Inventory.objects.filter(category="Beverage", quantity__gte=1)
        context = {"sch": sch}
    elif data == "Dairy_products":
        sch = Inventory.objects.filter(category="Dairy_products", quantity__gte=1)
        context = {"sch": sch}
    elif data == "Snacks":
        sch = Inventory.objects.filter(category="Snacks", quantity__gte=1)
        context = {"sch": sch}
    #print("yor are", request.session.get('email'))
    if(request.session.get('email') == None):
        return redirect("login")
    else :
        if (allD == None and obj == None ) :
            return render(request, "show_items.html", context)
        else :
            if(allD == None ) :
                return redirect("ownerHome")
            else :
                return redirect("employeeHome")


def search(request):
    query = request.GET["query"]  # query is the name of input tag
    allD = Inventory.objects.filter(
        item_name__icontains=query,
        quantity__gte=1
    )  # icontains is case insensitive and searches by word
    context = {"allD": allD}
    return render(request, "searchItems.html", context)



@login_required(login_url="login")
def cart(request, id):
    post = Cart()
    current_user = request.user
    post.user_email = current_user.email
    post.item_id = id
    post.quantity = 1
    post.save()
    #print (request.session.get('email'))
    return redirect("show_items")

@login_required(login_url="login")
def show_cart(request):
    email = request.session.get('email')
    sch = Employee.objects.filter(email=email).first()
    obj = Owner.objects.filter(email=email).first()
    
    AllD = Cart.objects.filter(user_email=request.user.email).all()
    context = {"AllD": AllD}
    if (sch == None and obj == None ) :
        return render(request, "show_cart.html", context)
    else :
        if(sch == None ) :
            return redirect("ownerHome")
        else :
            return redirect("employeeHome")


def delete_item_in_cart(request, id):
    obj = Cart.objects.get(cart_id=id)
    obj.delete()
    return redirect("show_cart")


#------------------------------------------------Owner-------------------------------------------------------------------


@login_required(login_url="login")
def ownerHome(request):
    email = request.session.get('email')
    obj = Owner.objects.filter(email=email).first()
    if(request.session.get('email') == None):
        return redirect("login")
    elif(obj == None) : 
        return redirect("login")
    else :
        return render(request, "ownerHome.html")

@login_required(login_url="login")
def show_items_owner(request, data=None):
    email = request.session.get('email')
    obj = Owner.objects.filter(email=email).first()
    if data == None or data == "All_Products":
        sch = Inventory.objects.all()
        context = {"sch": sch}
    elif data == "Beverage":
        sch = Inventory.objects.filter(category="Beverage")
        context = {"sch": sch}
    elif data == "Dairy_products":
        sch = Inventory.objects.filter(category="Dairy_products")
        context = {"sch": sch}
    elif data == "Snacks":
        sch = Inventory.objects.filter(category="Snacks")
        context = {"sch": sch}
    if(request.session.get('email') == None):
        return redirect("login")
    elif(obj == None) : 
        return redirect("login")
    else :
        return render(request, "show_items_owner.html", context)


@login_required(login_url="login")
def add_item_owner(request):
    email = request.session.get('email')
    obj = Owner.objects.filter(email=email).first()

    if request.method == "POST":
        post = Inventory()
        post.item_name = request.POST.get("item_name")
        post.quantity = request.POST.get("quantity")
        post.required_quantity = request.POST.get("required_quantity")
        post.category = request.POST.get("category")
        post.price = request.POST.get("price")
        post.save()
        return redirect("add_item_owner")

    else:
        if(request.session.get('email') == None):
            return redirect("login")
        elif(obj == None) : 
            return redirect("login")
        else :
            return render(request, "add_item_owner.html")


@login_required(login_url="login")
def update_item_owner(request, id):
    email = request.session.get('email')
    sch = Owner.objects.filter(email=email).first()
    obj = Inventory.objects.get(item_id=id)
    if request.method == "POST":
        obj.item_name = request.POST.get("item_name")
        obj.quantity = request.POST.get("quantity")
        obj.required_quantity = request.POST.get("required_quantity")
        obj.category = request.POST.get("category")
        obj.price = request.POST.get("price")
        obj.save()
        return redirect("show_items_owner")
    else:
        if(request.session.get('email') == None):
            return redirect("login")
        elif(sch == None) : 
            return redirect("login")
        else :
            return render(request, "update_item_owner.html", {"obj": obj})


@login_required(login_url="login")
def delete_items_owner(request, id):
    obj = Inventory.objects.get(item_id=id)
    obj.delete()
    return redirect("show_items_owner")

@login_required(login_url="login")
def add_employee(request):
    email = request.session.get('email')
    obj = Owner.objects.filter(email=email).first()
    if request.method == "POST":

        post = Employee()
        post.name = request.POST.get("name")
        post.email = request.POST.get("email")
        post.phone_number = request.POST.get("phone_number")
        post.save()
        return redirect("add_employee")

    else:
        if(request.session.get('email') == None):
            return redirect("login")
        elif(obj == None) : 
            return redirect("login")
        else :
            return render(request, "addEmployee.html")


@login_required(login_url="login")
def show_employee(request):
    email = request.session.get('email')
    obj = Owner.objects.filter(email=email).first()
    allD = Employee.objects.all()
    context = {"allD": allD}
    if(request.session.get('email') == None):
        return redirect("login")
    elif(obj == None) : 
        return redirect("login")
    else :
        return render(request, "show_employee.html", context)

@login_required(login_url="login")
def delete_employee(request, id):
    obj = Employee.objects.get(employee_id=id)
    obj.delete()
    return redirect("show_employee")


#----------------------------------------------Employee--------------------------------------------------------------


@login_required(login_url="login")
def empHome(request):
    email = request.session.get('email')
    obj = Employee.objects.filter(email=email).first()
    if(request.session.get('email') == None):
        return redirect("login")
    elif(obj == None) : 
        return redirect("login")
    else :
        return render(request, "employeeHome.html")


@login_required(login_url="login")
def show_items_employee(request, data=None):
    email = request.session.get('email')
    obj = Employee.objects.filter(email=email).first()
    if data == None or data == "All_Products":
        sch = Inventory.objects.all()
        context = {"sch": sch}
    elif data == "Beverage":
        sch = Inventory.objects.filter(category="Beverage")
        context = {"sch": sch}
    elif data == "Dairy_products":
        sch = Inventory.objects.filter(category="Dairy_products")
        context = {"sch": sch}
    elif data == "Snacks":
        sch = Inventory.objects.filter(category="Snacks")
        context = {"sch": sch}
    if(request.session.get('email') == None):
        return redirect("login")
    elif(obj == None) : 
        return redirect("login")
    else :
        return render(request, "show_items_employee.html", context)


@login_required(login_url="login")
def add_item_employee(request):
    email = request.session.get('email')
    obj = Employee.objects.filter(email=email).first()
    if request.method == "POST":

        post = Inventory()
        post.item_name = request.POST.get("item_name")
        post.quantity = request.POST.get("quantity")
        post.required_quantity = request.POST.get("required_quantity")
        post.category = request.POST.get("category")
        post.price = request.POST.get("price")
        post.save()
        return redirect("add_item_employee")

    else:
        if(request.session.get('email') == None):
            return redirect("login")
        elif(obj == None) : 
            return redirect("login")
        else :
            return render(request, "add_item_employee.html")
    


def delete_items_employee(request, id):
    obj = Inventory.objects.get(item_id=id)
    obj.delete()
    return redirect("show_items_employee")


@login_required(login_url="login")
def update_item_employee(request, id):
    email = request.session.get('email')
    sch = Employee.objects.filter(email=email).first()
    obj = Inventory.objects.get(item_id=id)
    if request.method == "POST":

        obj.item_name = request.POST.get("item_name")
        obj.quantity = request.POST.get("quantity")
        obj.required_quantity = request.POST.get("required_quantity")
        obj.category = request.POST.get("category")
        obj.price = request.POST.get("price")
        obj.save()
        return redirect("show_items_employee")
    else:
        if(request.session.get('email') == None):
            return redirect("login")
        elif(sch == None) : 
            return redirect("login")
        else :
            return render(request, "update_item_employee.html", {"obj": obj})


