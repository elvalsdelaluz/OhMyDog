from django.shortcuts import render, HttpResponse, redirect
import stripe
from .models import Donante, donacion
from .forms import FormularioDonacion
from datetime import date
stripe.api_key = 'sk_test_51NDyipASwHsRVYQPpkXqv817i0EKf3ojSo1HJJzrxEioHNaSRvADh1CCt15p6ubERTxZWur6JBYpKH8sclckfVzW00c3ehlY9Z'


#hacer vista de pago exitoso


def ya_esta_publicado(motivo, descripcion): 
    '''Se verifica si hay una camapaña con la misma descripción y motivo. En caso afirmativo devuelve true; negativo, false.'''
    existe_camapaña = False
    campañas = donacion.objects.all()

    if campañas.exists():
        for campaña in campañas:
            if (campaña.motivo == motivo) and (campaña.descripcion == descripcion):
                existe_camapaña = True
                break
    return existe_camapaña

def vista_subir_donacion(request):
    '''se procesa la info de la plantilla subir_donacion.html'''
    formulario = FormularioDonacion()
    if request.method=='POST':
        formulario = FormularioDonacion(data=request.POST)
        if formulario.is_valid():
            if (ya_esta_publicado(formulario.cleaned_data['motivo'],formulario.cleaned_data['descripcion'])):
                return render (request, 'donacion/subir_donacion.html',{'formulario':formulario, "mensaje2":"Ya ha publicado una camapaña con ese motivo y descripción."})
            else:
                nueva_donacion = donacion()
                nueva_donacion.motivo = formulario.cleaned_data['motivo']
                nueva_donacion.descripcion = formulario.cleaned_data['descripcion']
                #nueva_donacion.imagen = formulario.cleaned_data['imagen']
                nueva_donacion.finalizacion = formulario.cleaned_data['finalizacion']
                nueva_donacion.save()
                return redirect("donaciones")
    
    return render(request, 'donacion/subir_donacion.html', {'formulario': formulario})


def vista_donaciones (request):
    '''se hace un filtro por si se venció alguna donación y no debe mostrarse'''
    donaciones = donacion.objects.filter(finalizada=False)

    if (donaciones.filter(finalizacion__lte=date.today()).exists()):
        donaciones_vencidas=donaciones.filter(finalizacion__lte=date.today())
        donaciones_vencidas.update(finalizada=True)
        donaciones = donacion.objects.filter(finalizada=False)

    

    return render(request, "donacion/donaciones.html", {"donaciones":donaciones})



def vista_donar (request, donacion_id):
    '''se procesa la info de la plantilla donar.html'''
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