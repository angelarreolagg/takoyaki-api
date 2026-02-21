from decouple import config
import json
from openai import OpenAI


client = OpenAI(api_key=config("OPENAI_API_KEY"))


def rewrite_entry_with_ai(raw_entry):
    """
    It takes a raw JSON new entry and rewrites it to the defined format and style.
    """

    system_prompt = (
        "Eres un redactor estrella de un blog de noticias de anime y cultura geek. "
        "Tu estilo es dinámico, divertido y usas referencias que solo un verdadero fan entendería. "
        "Tu objetivo es transformar noticias de otros sitios para que sean contenido original, "
        "evitando el plagio pero manteniendo la veracidad de los hechos."
    )

    user_prompt = f"""
    Reescribe la siguiente noticia basándote en estos datos:
    Título Original: {raw_entry.get('title')}
    Subtítulo: {raw_entry.get('subtitle')}
    Subtitulos: {raw_entry.get('info_subtitles')}
    Contenido: {raw_entry.get('info_data')}
    
    Instrucciones específicas:
    1. Crea un título que genere curiosidad (clickbait sano).
    2. Divide el contenido en bloques lógicos (toma los Subtitulos como referencia).
    3. Devuelve la respuesta estrictamente en formato JSON con esta estructura:
    {{
        "title": "string",
        "subtitle": "string",
        "content_blocks": [
            {{ "type": "text", title: "text", "value": "párrafo 1..." }},
            {{ "type": "text", title: "text", "value": "párrafo 2..." }},
            {{ "type": "fact", title: "text", "value": "dato curioso sobre el anime mencionado" }}
        ],
        "tags": ["lista", "de", "tags"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"Error calling the OpenAI API or transforming the object: {e}")
        return None
