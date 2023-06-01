from django.shortcuts import render, HttpResponse, redirect
import stripe
from .models import Donante, donacion
from .forms import FormularioDonacion
stripe.api_key = 'sk_test_51NDyipASwHsRVYQPpkXqv817i0EKf3ojSo1HJJzrxEioHNaSRvADh1CCt15p6ubERTxZWur6JBYpKH8sclckfVzW00c3ehlY9Z'


#hacer vista de pago exitoso

#no se como hacer para que la donacion, cuando pasa el tiempo, se cierre sola.
def vista_subir_donacion(request):
    formulario = FormularioDonacion()
    if request.method=='POST':
        formulario = FormularioDonacion(data=request.POST)
        if formulario.is_valid():
            nueva_donacion = donacion()
            nueva_donacion.motivo = formulario.cleaned_data['motivo']
            nueva_donacion.descripcion = formulario.cleaned_data['descripcion']
            #nueva_donacion.imagen = formulario.cleaned_data['imagen']
            nueva_donacion.finalizacion = formulario.cleaned_data['finalizacion']
            nueva_donacion.save()
            return redirect("donaciones")
    else:
        return render(request, "donacion/subir_donacion.html", {'formulario': formulario})


def vista_donaciones (request):
    donaciones = donacion.objects.all()
    return render(request, "donacion/donaciones.html", {"donaciones":donaciones})



def vista_donar (request, donacion_id):
    dona = donacion.objects.get(id=donacion_id)

    if request.method == "POST":
        amount = int(request.POST["amount"]) 
        #Create customer
        try:
            if request.user.is_authenticated:
                customer = stripe.Customer.create(
                            email=request.user.email,
			                name=request.user.nombre,
                            description="Test donation",
                            source=request.POST['stripeToken']
                                )
            else:
                customer = stripe.Customer.create(
                            source=request.POST['stripeToken']
                                )
        except stripe.error.CardError as e:
            if e.code == 'card_declined':
                if "insufficient funds" in str(e).lower():
                    return HttpResponse("no tenes plata papá") #redirigir a otro lado con msg de error. esto es muy villero                    
            return HttpResponse("ocurrió un problema con la tarjeta durante el pago, intente mas tarde") #se puede hacer que se trate el error de codigo de seguridad
                     
        ###errores randoms sin importancia
        except stripe.error.RateLimitError as e:
                # handle this e, which could be stripe related, or more generic
                return HttpResponse("<h1>Rate error!</h1>")

        except stripe.error.InvalidRequestError as e:
            return HttpResponse("<h1>Invalid requestor!</h1>")

            
        

        except stripe.error.AuthenticationError as e:  
            return HttpResponse("<h1>Invalid API auth!</h1>")

        except stripe.error.StripeError as e:  
            return HttpResponse("<h1>Stripe error!</h1>")

        except Exception as e:  
            pass  

        
        #Stripe charge 
        charge = stripe.Charge.create(
                    customer=customer,
                    amount=int(amount)*100,
                    currency='usd',
                    description="Test donation"
                ) 
        transRetrive = stripe.Charge.retrieve(
                    charge["id"],
                    api_key="sk_test_51NDyipASwHsRVYQPpkXqv817i0EKf3ojSo1HJJzrxEioHNaSRvADh1CCt15p6ubERTxZWur6JBYpKH8sclckfVzW00c3ehlY9Z"
                )
        charge.save() # Uses the same API Key.
        if request.user.is_authenticated:
            nuevo_donante = Donante()
            nuevo_donante.dueño = request.user
            nuevo_donante.monto = amount=int(amount)
            nuevo_donante.save()
        #return redirect("pay_success/")
        return redirect("home")

                   


    return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo})