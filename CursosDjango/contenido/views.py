from django.shortcuts import render,HttpResponse

menu="""
    <p>Selecciona una opción:</p>
    <a href="/">Inicio</a>
    <a href="/cursos/">Cursos</a> 
    <a href="/contacto/">Contacto</a>
    """

# Create your views here.
def principal(request):
    contenido="<h1>Bienvenido a Cursos Django</h1>"
    return HttpResponse(menu+contenido)

def cursos(request):
    contenido="""<h1>Cursos disponibles</h1>
        <ul>
            <li>Programación</li>
            <li>Bases de datos</li>
            <li>Desarrollo web</li>
        </ul> """
    return HttpResponse(menu+contenido)

def contacto(request):
        contenido="""<h1>Contacto</h1>
        <form>
            Nombre:<br>
            <input type="text"><br><br>
            Correo:<br>
            <input type="email"><br><br>
            Curso:<br>
            <select>
                <option>Programación</option>
                <option>Bases de datos</option>
                <option>Desarrollo web</option>
            </select><br><br>
            Comentarios:<br>
            <textarea></textarea><br><br>
            <button>Enviar</button>
        </form>
        <br>
    """
        return HttpResponse(menu+contenido)