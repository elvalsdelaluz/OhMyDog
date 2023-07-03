from django.shortcuts import render, HttpResponse, redirect
import stripe
from mascotas.models import Mascota
from .models import Donante, donacion, DonanteNoRegistrado
from .forms import FormularioDonacion,FormularioDonar
from datetime import date
from donacion.models import Tarjeta
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
    ##########################################################
    ###################BLOQUEO OPCION#########################
    usuario_autenticado = request.user
    if usuario_autenticado.is_authenticated and not usuario_autenticado.is_staff:
        #pregunto si tiene perros  
        tiene_perros = Mascota.objects.filter(dueño=usuario_autenticado).exists()
        if not tiene_perros:
            return redirect('alta_mascota')
    ##########################################################


    '''se hace un filtro por si se venció alguna donación y no debe mostrarse'''
    donacion_refugios= donacion.objects.filter(motivo='Donacion para refugios').get()
    donaciones = donacion.objects.filter(finalizada=False).exclude(motivo='Donacion para refugios')

    if (donaciones.filter(finalizacion__lte=date.today()).exists()):
        donaciones_vencidas=donaciones.filter(finalizacion__lte=date.today())
        donaciones_vencidas.update(finalizada=True)
        donaciones = donacion.objects.filter(finalizada=False).exclude(motivo='Donacion para refugios')

    

    return render(request, "donacion/donaciones.html", {"donaciones":donaciones, "refugios":donacion_refugios})

def ver_registro(request, donacion_id):

    donacion_ver= donacion.objects.get(id=donacion_id)

    donantes_clientes =Donante.objects.filter(campania_donacion=donacion_id)

    donantes_noclientes = DonanteNoRegistrado.objects.filter(campania_donacion=donacion_id)

    return render (request, "donacion/registro_donaciones.html",{"donacion":donacion_ver, "donantes_clientes":donantes_clientes, "donantes_noclientes":donantes_noclientes})


def vista_donar2 (request, donacion_id):
    formulario = FormularioDonar()
    dona = donacion.objects.get(id=donacion_id)
    if request.method == 'POST':
        
        formulario = FormularioDonar(request.POST)
        if formulario.is_valid():
            numero = formulario.cleaned_data['numero']
            try:
                tarjeta = Tarjeta.objects.get(numero=numero)
            except Exception as e:
                #no existe tarjeta
                return render(request,"donacion/donar2.html",{'formulario':formulario, "mensaje": "El número de tarjeta es inválido"})
            else:
            #caso que la tarjeta exista
                
                mensaje_error = ""
                if (formulario.cleaned_data['nombre_dueño'] != tarjeta.nombre_dueño):
                    mensaje_error += "El nombre ingresado no condice con el de la tarjeta.<br>"
                if (formulario.cleaned_data['codigo_seguridad'] != tarjeta.codigo_seguridad):
                    mensaje_error += "El código de seguridad es incorrecto.<br>"
                if (int(formulario.cleaned_data['mes_vencimiento']) != int(tarjeta.mes_vencimiento) or formulario.cleaned_data['año_vencimiento'] != tarjeta.año_vencimiento):
                    mensaje_error += "La fecha es incorrecta. (CAMBIAR EN PIVOTAL)<br>"
                print (mensaje_error)
                if mensaje_error != "":
                    return render(request,"donacion/donar2.html",{'formulario':formulario, "mensaje": mensaje_error})  

                if (formulario.cleaned_data['monto'] > tarjeta.saldo):
                    return render(request,"donacion/donar2.html",{'formulario':formulario, "mensaje": 'El saldo de la tarjeta es insuficiente'})  
                else:
                    tarjeta.saldo -= formulario.cleaned_data['monto']
                    tarjeta.save()

                if request.user.is_authenticated:
                    donante = request.user
                    donante.es_donante= True
                    donante.descuento_acumulado= donante.descuento_acumulado + (formulario.cleaned_data['monto']*20/100)
                    donante.save()
                    nuevo_donante = Donante()
                    nuevo_donante.campania_donacion= dona
                    nuevo_donante.dueño = request.user
                    nuevo_donante.monto = formulario.cleaned_data['monto']
                    nuevo_donante.save()
                else:
                    no_registrado = DonanteNoRegistrado()
                    no_registrado.campania_donacion= dona
                    no_registrado.nombre = formulario.cleaned_data['nombre_dueño']
                    no_registrado.monto = formulario.cleaned_data['monto']
                    no_registrado.save()
                #return redirect("pay_success/")
                return redirect("pago_realizado")              
    return render(request, "donacion/donar2.html", {'formulario':formulario,"donacion_motivo": dona.motivo})


'''
def vista_donar (request, donacion_id):
    #se procesa la info de la plantilla donar.html
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
                    return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo, "mensaje": "La tarjeta tiene saldo insuficiente."})

            elif e.code == 'incorrect_cvc':
                return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo, "mensaje": "El código de seguridad es incorrecto."}) 

            elif e.code == 'processing_error':
                return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo, "mensaje": "El nombre ingresado no condice con el de la tarjeta."}) 

            return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo, "mensaje": "Ha ocurrido un error con la tarjeta. Intente con otra."}) 

                     
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
            donante = request.user
            donante.es_donante= True
            donante.descuento_acumulado= donante.descuento_acumulado + (amount*20/100)
            donante.save()
            nuevo_donante = Donante()
            nuevo_donante.campania_donacion= dona
            nuevo_donante.dueño = request.user
            nuevo_donante.monto = amount=int(amount)
            nuevo_donante.save()
        else:
            no_registrado = DonanteNoRegistrado()
            no_registrado.campania_donacion= dona
            no_registrado.nombre = request.POST['nombre']
            no_registrado.monto = amount = int(amount)
            no_registrado.save()
        #return redirect("pay_success/")
        return redirect("pago_realizado")
    
    return render(request, "donacion/donar.html", {"donacion_motivo": dona.motivo})
'''




def vista_pago_realizado(request):
    return render(request, "donacion/pago_realizado.html")