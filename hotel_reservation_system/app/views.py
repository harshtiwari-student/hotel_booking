from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Room,Booking,Address,Payment
from django.db.models import Max

from datetime import datetime
from django.contrib import messages
# Create your views here.
def index(req):
    # allproducts=Product.objects.all()
    # context={"allproducts":allproducts}
    rooms = Room.objects.all()
    
    # Send rooms to the template
    return render(req, 'index.html', {'rooms': rooms})

def validate_password(password):
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check maximum length
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")

    # Initialize flags for character checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    # Check for character variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )

    # Check against common passwords
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ]  # Add more common passwords
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")


def signup(req):
    print(req.method)
    context = {}
    if req.method == "GET":
        return render(req, "signup.html")
    else:
        print(req.method)
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        print(uname, upass, ucpass)

        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context)

        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)
        elif uname.isdigit():
            context["errmsg"] = "Username can't be only number"
            return render(req, "signup.html", context)
        elif upass == uname:
            context["errmsg"] = "Password cannot same as username"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                print(User.objects.all())
                return redirect("signin")
            except:
                print("User already exists")
                context["errmsg"] = "User already exists"
                return render(req, "signup.html", context)


def signin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signin.html", context)
        else:
            userdata = authenticate(username=uname, password=upass)
            # print(req.user.password)
            if userdata is not None:
                login(req, userdata)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "signin.html", context)
    else:
        return render(req, "signin.html")
    
def userlogout(req):
    logout(req)
    return redirect("/")


def request_password_reset(req):
    if req.method == "GET":
        return render(req, "request_password_reset.html")
    else:
        uname = req.POST.get("uname")
        context = {}
        try:
            userdata = User.objects.get(username=uname)
            return redirect("reset_password", uname=userdata.username)

        except User.DoesNotExist:
            context["errmsg"] = "No account found with this username"
            return render(req, "request_password_reset.html", context)


def reset_password(req, uname):
    userdata = User.objects.get(username=uname)
    if req.method == "GET":
        return render(req, "reset_password.html", {"user": userdata.username})
    else:
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        userdata = User.objects.get(username=uname)
        try:
            if upass == "" or ucpass == "":
                context["errmsg"] = "Field can't be empty"
                return render(req, "reset_password.html", context)
            elif upass != ucpass:
                context["errmsg"] = "Password and confirm password need to match"
                return render(req, "reset_password.html", context)
            else:
                validate_password(upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("signin")

        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "reset_password.html", context)
        
def aboutus(req):
    return render(req,"aboutus.html")

def contact(req):
    return render(req,"contact.html")

from .models import Room     
from django.db.models import Q
from django.contrib import messages
def searchproduct(req):
    query=req.GET["q"]
    if query:
        rooms=Room.objects.filter(Q(roomid=query))

        if len(rooms)==0:
            messages.error(req,"No result found ")

    else:
        rooms=Room.objects.all()

    context={'rooms':rooms}
    return render (req,'index.html',context)


def home(request):
    # Fetch all rooms from the database
    rooms = Room.objects.all()
    # Send rooms to the template
    room_data = []
    for room in rooms:
        is_booked = Booking.objects.filter(roomid=room, roomid__is_available=False).exists()
        room_data.append({
            'room': room,
            'booked': is_booked
        })
    return render(request, 'index.html', {'rooms': rooms})



@login_required
def bookroom(request, roomid):
    room = get_object_or_404(Room, pk=roomid)

    if request.method == "POST":
        checkin = request.POST.get("checkin_date")
        checkout = request.POST.get("checkout_date")
        guests = int(request.POST.get("guests"))
        payment_method = request.POST.get("payment_method")

        checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date()
        checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date()
        nights = (checkout_date - checkin_date).days
        total_price = room.price_per_night * nights

        last_booking = Booking.objects.aggregate(Max('bookingid'))['bookingid__max'] or 0
        new_bookingid = last_booking + 1

        booking = Booking.objects.create(
            bookingid=new_bookingid,
            userid=request.user,
            roomid=room,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            guests=guests,
            payment_method=payment_method,
            totalprice=total_price,
        )
        

        # Store booking temporarily in session
        request.session["booking_data"] = {
            "roomid": room.roomid,
            "roomtype": room.roomtype,
        }
        # Store booking temporarily in session
        request.session["booking_data"] = {
            "roomid": room.roomid,
           "checkin_date": checkin,
            "checkout_date": checkout,
            "guests": guests,
            "payment_method": payment_method,
            "totalprice": total_price,
        }

        return redirect("final_payment")  # 👈 This goes to the payment summary page

    return render(request, "bookroom.html", {"room": room})



from datetime import datetime
from django.contrib import messages

@login_required
def final_payment(request):
    booking_data = request.session.get("booking_data")
    if not booking_data:
        return render(request, 'final_payment.html', {'booking': None})

    return render(request, "final_payment.html", {
        "booking": booking_data
    })
    

# crud operation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Room

class RoomRegister(CreateView):
    model = Room
    fields = ["roomid", "description", "price_per_night"]
    success_url = '/room-list/'

    def form_valid(self, form):
        form.instance.user = self.request.user  # assuming Room has a 'user' ForeignKey
        return super().form_valid(form)

class RoomList(ListView):
    model = Room

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(user=user)

class RoomDelete(DeleteView):
    model = Room
    success_url = '/room-list/'

class RoomUpdate(UpdateView):
    model = Room
    template_name_suffix = "_update_form"
    fields = ["room_name", "category", "description", "price", "images"]
    success_url = '/room-list/'











