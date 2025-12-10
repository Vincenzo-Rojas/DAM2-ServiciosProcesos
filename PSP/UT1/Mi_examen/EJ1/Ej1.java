package Ej1;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Ej1 {
    public static void main(String[] args) {
        // Descomentar para iniciar pruebas
        //crearBiblioteca();
        //listarGeneros();
        //videojuegoMejorPuntuado();
        //agregarVideojuego();

    }

    public static void crearBiblioteca() {

        Scanner sc = new Scanner(System.in);

        int id = 0;

        String titulo = null;

        String plataforma = null; // PC, PlayStation, Xbox, Nintendo Switch
        String lPlataforma = "pc,playStation,xbox,nintendo switch";
        String[] listaPlataforma = lPlataforma.split(",");
        boolean correctoP = false;

        int yearLaunch;

        String genero = null; // accion, rpg, estrategia, aventura, deportes
        String lGenero = "accion,rpg,estrategia,aventura,deportes";
        String[] listaGenero = lGenero.split(",");
        boolean correctoG = false;

        Double precio;
        double puntuacionCriticos;

        try {
            System.out.println("\n--- MENÚ XML ---");
            System.out.println("Dime titulo");
            titulo = sc.nextLine().trim();

            System.out.println("Dime plataforma:");
            plataforma = sc.nextLine().trim().toLowerCase();
            for (int i = 0; i<listaPlataforma.length;i++){
                if(listaPlataforma[i].equals(plataforma)){
                    correctoP = true;
                }
            }
            if (correctoP == false){
                System.out.println("No se ha indicado la plataforma correcta");
                return;
            }


            System.out.println("Dime el ayo de lanzamiento");
            yearLaunch = sc.nextInt();
            sc.nextLine(); // limpiar buffer

            System.out.println("Dime el genero");
            genero = sc.nextLine().trim().toLowerCase(Locale.ROOT);
            for (int i = 0; i<listaGenero.length;i++){
                if(listaGenero[i].equals(genero)){
                        correctoG = true;
                }
            }
            if (correctoG == false){
                System.out.println("No se ha indicado el genero correcto");
                return;
            }

            System.out.println("Dime el precio");
            precio = sc.nextDouble();
            sc.nextLine(); // limpiar buffer
            if (precio <0 ){
                System.out.println("El precio tiene que ser superior a 0");
                return;
            }

            System.out.println("Dime la puntuacion de la critica");
            puntuacionCriticos = sc.nextDouble();
            sc.nextLine(); // limpiar buffer
            if (puntuacionCriticos <0 || puntuacionCriticos >10){
                System.out.println("La puntuacion critica es entre 0 y 10");
                return;
            }

            sc.close();

            //Crear xml
            try {
                // Creamos el builder
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();

                Document doc = builder.newDocument();
                Element root = doc.createElement("biblioteca"); // Creamos elemento raíz

                doc.appendChild(root); // Añadimos la raíz al documento

                //formatear el id
                id += 1;
                String idString = id + "";

                // crear <videojuego>
                Element videojuego = doc.createElement("videojuego");
                videojuego.setAttribute("id", idString.trim());
                videojuego.setAttribute("plataforma", plataforma);

                //etiquetas del videojuego + el texto que llevan dentro
                Element tituloE = doc.createElement("Titulo");
                tituloE.setTextContent(titulo); // texto dentro de <title>

                Element ayoE = doc.createElement("Ayo");
                ayoE.setTextContent(yearLaunch+"");

                Element generoE = doc.createElement("Genero");
                generoE.setTextContent(genero);

                Element precioE = doc.createElement("Precio");
                precioE.setTextContent(precio+"");

                Element puntuacionE = doc.createElement("Puntuacion");
                puntuacionE.setTextContent(puntuacionCriticos+"");

                //Add elementos al videojuego
                videojuego.appendChild(tituloE);
                videojuego.appendChild(ayoE);
                videojuego.appendChild(generoE);
                videojuego.appendChild(precioE);
                videojuego.appendChild(puntuacionE);

                root.appendChild(videojuego);

                // Guardamos el documento en disco (escritura del archivo XML)
                // Escribimos de nuevo el fichero
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer t = tf.newTransformer();
                t.setOutputProperty(OutputKeys.INDENT, "yes");

                DOMSource src = new DOMSource(doc);
                StreamResult result = new StreamResult(Paths.get( "biblioteca_videojuegos.xml").toFile());

                t.transform(src, result);

            } catch (ParserConfigurationException e) {
                System.err.println("Error configurando el parser XML: " + e.getMessage());
                e.printStackTrace();
            } catch (TransformerException e) {
                System.err.println("Error guardando el XML modificado: " + e.getMessage());
                e.printStackTrace();
            }

        }catch (Exception e){
            e.printStackTrace();
        }
    }

    //Muestra los generos diferentes sin repetir
    public static void listarGeneros(){
        HashSet<String> listaGeneros = new HashSet<>(); // No se añaden elemntos repetidos
        String rutaArchivo = "biblioteca_videojuegos.xml";
        try {

            // Crear un objeto Path moderno a partir de la ruta proporcionada como parámetro
            Path rutaXML = Path.of(rutaArchivo);

            // Comprobar si el archivo existe; si no, mostrar error y salir del método
            if (!Files.exists(rutaXML)) {
                System.err.println("No se encontró el archivo XML: " + rutaXML.toAbsolutePath());
                return; // Sale del método si el archivo no existe
            }

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(rutaXML.toFile());

            // Normalizar el documento combina nodos de texto adyacentes y limpia espacios
            doc.getDocumentElement().normalize();

            // OBTENER TODAS LAS SECCIONES
            // NodeList con todos los nodos <Genero> del documento
            NodeList secciones = doc.getElementsByTagName("Genero");

            System.out.println("Mostrar generos diferentes sin repetir:");

            // Iterar por cada nodo <section> encontrado
            for (int i = 0; i < secciones.getLength(); i++) {
                Node nodo = secciones.item(i); // Obtener el nodo i
                // Comprobar que el nodo es de tipo ELEMENT_NODE (evitar nodos de texto u otros tipos)
                if (nodo.getNodeType() == Node.ELEMENT_NODE) {
                    Element eSeccion = (Element) nodo; // Convertir a Element para acceder a atributos
                    String generoContent = eSeccion.getTextContent(); // Leer texto del genero
                    listaGeneros.add(generoContent); // add geneto texto(Pc,rpg...)
                }
            }

        } catch (ParserConfigurationException e) {
            // Se lanza si falla la configuración del parser DOM
            e.printStackTrace();
        } catch (SAXException e) {
            // Se lanza si el XML está mal formado o no se puede parsear
            e.printStackTrace();
        } catch (IOException e) {
            // Se lanza si hay errores de lectura/escritura de archivos
            e.printStackTrace();
        }

        System.out.println(listaGeneros);
    }

    //devulve y muestra el titulo mejor puntuado
    public static String videojuegoMejorPuntuado(){

        // Crear un diccionario (clave → valor)
        Map<String, Double> diccionario = new HashMap<>();
        String rutaArchivo = "biblioteca_videojuegos.xml";

        try {
            // Crear un objeto Path moderno a partir de la ruta proporcionada como parámetro
            Path rutaXML = Path.of(rutaArchivo);

            // Comprobar si el archivo existe; si no, mostrar error y salir del método
            if (!Files.exists(rutaXML)) {
                System.err.println("No se encontró el archivo XML: " + rutaXML.toAbsolutePath());
                return null; // Sale del método si el archivo no existe
            }

            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(rutaXML.toFile());

            // Normalizar el documento combina nodos de texto adyacentes y limpia espacios
            doc.getDocumentElement().normalize();

            // OBTENER: juego con mejor puntuacion - juego1
            // NodeList con todos los nodos <videojuego> del documento
            NodeList videojuego = doc.getElementsByTagName("videojuego");

            System.out.println("\nOBTENER: juego con mejor puntuacion:");

            // Iterar por cada nodo <videojuego> encontrado
            for (int i = 0; i < videojuego.getLength(); i++) {
                Node nodo = videojuego.item(i); // Obtener el nodo i
                // Comprobar que el nodo es de tipo ELEMENT_NODE (evitar nodos de texto u otros tipos)
                if (nodo.getNodeType() == Node.ELEMENT_NODE) {
                    Element eSeccion = (Element) nodo; // Convertir a Element para acceder a atributos

                    String tituloText = eSeccion.getElementsByTagName("Titulo").item(0).getTextContent();
                    Double puntuacionNum = Double.parseDouble(eSeccion.getElementsByTagName("Puntuacion").item(0).getTextContent());

                    diccionario.put(tituloText, puntuacionNum);
                }
            }
        } catch (ParserConfigurationException e) {
            // Se lanza si falla la configuración del parser DOM
            e.printStackTrace();
        } catch (SAXException e) {
            // Se lanza si el XML está mal formado o no se puede parsear
            e.printStackTrace();
        } catch (IOException e) {
            // Se lanza si hay errores de lectura/escritura de archivos
            e.printStackTrace();
        } catch (NumberFormatException e){
            e.printStackTrace();
        }

        // Calcular la mayor puntuacion
        double max = -1;
        String titulo = null;

        for (Map.Entry<String, Double> entrada : diccionario.entrySet()) {
            double uso = entrada.getValue();
            if (uso > max) {
                max = uso;
                titulo = entrada.getKey();
            }
        }

        if (titulo != null) {
            System.out.println("El máximo puntuacion es " + max + " del videojuego: " + titulo);
            return titulo;
        } else {
            System.out.println("No se encontraron datos válidos.");
        }

        return null;
    }

    public static void agregarVideojuego(){
        String rutaArchivo = "biblioteca_videojuegos.xml";
        Scanner sc = new Scanner(System.in);

        int id = 0;

        String titulo = null;

        String plataforma = null; // PC, PlayStation, Xbox, Nintendo Switch
        String lPlataforma = "pc,playStation,xbox,nintendo switch";
        String[] listaPlataforma = lPlataforma.split(",");
        boolean correctoP = false;

        int yearLaunch;

        String genero = null; // accion, rpg, estrategia, aventura, deportes
        String lGenero = "accion,rpg,estrategia,aventura,deportes";
        String[] listaGenero = lGenero.split(",");
        boolean correctoG = false;

        Double precio;
        double puntuacionCriticos;

        try {
            System.out.println("\n--- MENÚ XML ---");
            System.out.println("Dime titulo");
            titulo = sc.nextLine().trim();

            System.out.println("Dime plataforma:");
            plataforma = sc.nextLine().trim().toLowerCase();
            for (int i = 0; i<listaPlataforma.length;i++){
                if(listaPlataforma[i].equals(plataforma)){
                    correctoP = true;
                }
            }
            if (correctoP == false){
                System.out.println("No se ha indicado la plataforma correcta");
                return;
            }


            System.out.println("Dime el ayo de lanzamiento");
            yearLaunch = sc.nextInt();
            sc.nextLine(); // limpiar buffer

            System.out.println("Dime el genero");
            genero = sc.nextLine().trim().toLowerCase(Locale.ROOT);
            for (int i = 0; i<listaGenero.length;i++){
                if(listaGenero[i].equals(genero)){
                    correctoG = true;
                }
            }
            if (correctoG == false){
                System.out.println("No se ha indicado el genero correcto");
                return;
            }

            System.out.println("Dime el precio");
            precio = sc.nextDouble();
            sc.nextLine(); // limpiar buffer
            if (precio <0 ){
                System.out.println("El precio tiene que ser superior a 0");
                return;
            }

            System.out.println("Dime la puntuacion de la critica");
            puntuacionCriticos = sc.nextDouble();
            sc.nextLine(); // limpiar buffer
            if (puntuacionCriticos <0 || puntuacionCriticos >10){
                System.out.println("La puntuacion critica es entre 0 y 10");
                return;
            }

            sc.close();

            //Modificar xml
            try {
                // Crear un objeto Path moderno a partir de la ruta proporcionada como parámetro
                Path rutaXML = Path.of(rutaArchivo);

                // Comprobar si el archivo existe; si no, mostrar error y salir del método
                if (!Files.exists(rutaXML)) {
                    System.err.println("No se encontró el archivo XML: " + rutaXML.toAbsolutePath());
                    return; // Sale del método si el archivo no existe
                }

                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder = factory.newDocumentBuilder();
                Document doc = builder.parse(rutaXML.toFile());

                // Normalizar el documento combina nodos de texto adyacentes y limpia espacios
                doc.getDocumentElement().normalize();

                //Agregar videojuego

                //Buscar el ultimo id
                int idUltimo = 0;
                NodeList sections = doc.getElementsByTagName("videojuego");

                for (int i = 0; i < sections.getLength(); i++) {
                    Node nodo = sections.item(i);
                    if (nodo.getNodeType() == Node.ELEMENT_NODE) {
                        Element e = (Element) nodo;
                        int idUltimoT = Integer.parseInt(e.getAttribute("id"));
                        if (idUltimo < idUltimoT){
                            idUltimo = idUltimoT;
                        }
                    }
                }

                if (idUltimo == 0) {
                    System.out.println("No se encontró ninguna seccion <videojuego>");
                    return;
                }


                // Crear el nuevo videojuego

                // crear <videojuego>
                Element videojuego = doc.createElement("videojuego");
                videojuego.setAttribute("id", (idUltimo+1)+"");
                videojuego.setAttribute("plataforma", plataforma);

                //etiquetas del videojuego + el texto que llevan dentro
                Element tituloE = doc.createElement("Titulo");
                tituloE.setTextContent(titulo); // texto dentro de <title>

                Element ayoE = doc.createElement("Ayo");
                ayoE.setTextContent(yearLaunch+"");

                Element generoE = doc.createElement("Genero");
                generoE.setTextContent(genero);

                Element precioE = doc.createElement("Precio");
                precioE.setTextContent(precio+"");

                Element puntuacionE = doc.createElement("Puntuacion");
                puntuacionE.setTextContent(puntuacionCriticos+"");

                //Add elementos al videojuego
                videojuego.appendChild(tituloE);
                videojuego.appendChild(ayoE);
                videojuego.appendChild(generoE);
                videojuego.appendChild(precioE);
                videojuego.appendChild(puntuacionE);

                doc.getDocumentElement().appendChild(videojuego);


                // Guardar los cambios en el archivo
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer transformer = tf.newTransformer();

                // Fuente y resultado
                DOMSource source = new DOMSource(doc);
                // Si no existe el archivo se crea
                StreamResult result = new StreamResult(Paths.get( "biblioteca_videojuegos_actualizada.xml").toFile());

                transformer.setOutputProperty(OutputKeys.INDENT, "yes");
                transformer.transform(source, result);

                System.out.println("Añadido nuevo videojuego");

            } catch (ParserConfigurationException e) {
                System.err.println("Error configurando el parser XML: " + e.getMessage());
                e.printStackTrace();
            } catch (TransformerException e) {
                System.err.println("Error guardando el XML modificado: " + e.getMessage());
                e.printStackTrace();
            }

        }catch (Exception e){
            e.printStackTrace();
        }
    }

}


