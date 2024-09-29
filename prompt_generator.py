
NUM_QD = 5
NUM_OD = 2

def get_question_domains_prompt(question):
    question_domain_format = "Medical Field: " + " | ".join(["Field" + str(i) for i in range(NUM_QD)])
    question_classifier = "Eres un experto médico especializado en clasificar un escenario médico en áreas específicas de la medicina."
    prompt_get_question_domain = f"Debes completar los siguientes pasos:" \
            f"1. Lee cuidadosamente el escenario médico presentado en la pregunta: '''{question}'''. \n" \
            f"2. Basado en el escenario médico, clasifica la pregunta en cinco subcampos diferentes de la medicina. \n" \
            f"3. Debes entregar el resultado en exactamente el mismo formato que '''{question_domain_format}'''."
    return question_classifier, prompt_get_question_domain

def get_question_analysis_prompt(question, question_domain):
    question_analyzer = f"Eres un experto médico en el campo de {question_domain}. " \
        f"Desde tu área de especialización, examinarás y diagnosticarás los síntomas presentados por los pacientes en escenarios médicos específicos."
    prompt_get_question_analysis = f"Por favor, examina meticulosamente el escenario médico descrito en esta pregunta: '''{question}'''. " \
                        f"Basándote en tu experiencia médica, interpreta la condición que se está describiendo. " \
                        f"Posteriormente, identifica y resalta los aspectos del problema que consideres más alarmantes o relevantes."

    return question_analyzer, prompt_get_question_analysis


def get_options_domains_prompt(question, options):
    options_domain_format = "Medical Field: " + " | ".join(["Field" + str(i) for i in range(NUM_OD)])
    options_classifier = f"Como experto médico, posees la capacidad de identificar los dos campos de especialización más relevantes necesarios para abordar una pregunta de opción múltiple que encapsula un contexto médico específico."
    prompt_get_options_domain = f"Debes completar los siguientes pasos:" \
                f"1. Lee cuidadosamente el escenario médico presentado en la pregunta: '''{question}'''." \
                f"2. Las opciones disponibles son: '''{options}'''. Esfuérzate por entender las conexiones fundamentales entre la pregunta y las opciones." \
                f"3. Tu objetivo principal debe ser clasificar las opciones en dos subcampos distintos de la medicina. " \
                f"Debes entregar el resultado en exactamente el mismo formato que '''{options_domain_format}'''."
    return options_classifier, prompt_get_options_domain



def get_options_analysis_prompt(question, options, op_domain, question_analysis):
    option_analyzer = f"Eres un experto médico especializado en el campo de {op_domain}. " \
                f"Eres hábil para comprender la relación entre las preguntas y las opciones en exámenes de opción múltiple, y para determinar su validez. " \
                f"Tu tarea específica es analizar cada opción utilizando tu conocimiento médico especializado y evaluar su relevancia y corrección."

    prompt_get_options_analyses = f"Con respecto a la pregunta: '''{question}''', obtuvimos el análisis de cinco expertos de diversos campos. \n"
    for _domain, _analysis in question_analysis.items():
        prompt_get_options_analyses += f"La evaluación del experto en {_domain} sugiere: {_analysis} \n"
        prompt_get_options_analyses += f"Las siguientes son las opciones disponibles: '''{options}'''." \
                    f"Revisando el análisis de la pregunta por parte del equipo de expertos, se te pide que comprendas la relación entre las opciones y la pregunta desde la perspectiva de tu respectivo campo, " \
                    f"y analices cada opción individualmente para evaluar si es plausible o debe ser eliminada con base en la razón y la lógica. "\
                    f"Presta especial atención a las diferencias entre las distintas opciones y justifica su existencia. " \
                    f"Algunas de estas opciones pueden parecer correctas a primera vista, pero podrían ser engañosas en realidad."
    return option_analyzer, prompt_get_options_analyses



def get_final_answer_prompt_analonly(question, options, question_analyses, option_analyses):
    prompt = f"Pregunta: {question} \nOpciones: {options} \n" \
        f"Respuesta: Vamos a resolver esto paso a paso para asegurarnos de tener la respuesta correcta. \n" \
        f"Paso 1: Decodificar correctamente la pregunta. Contamos con un equipo de expertos que han realizado un análisis detallado de esta pregunta. " \
        f"El equipo incluye cinco expertos de diferentes dominios médicos relacionados con el problema. \n"
    
    for _domain, _analysis in question_analyses.items():
        prompt += f"La opinión de un experto en {_domain} sugiere: {_analysis} \n"
    
    prompt += f"Paso 2: Evalúa cada opción presentada individualmente, basándote tanto en los detalles del escenario del paciente como en tu conocimiento médico. " \
            f"Presta especial atención a las diferencias entre las distintas opciones. " \
            f"Algunas de estas opciones pueden parecer correctas a primera vista, pero podrían ser engañosas en realidad. " \
            f"Contamos con análisis detallados de expertos en dos dominios. \n"
    
    for _domain, _analysis in option_analyses.items():
        prompt += f"La evaluación de un experto en {_domain} sugiere: {_analysis} \n"
    
    prompt += f"Paso 3: Basado en la comprensión obtenida de los pasos anteriores, selecciona la opción óptima para responder la pregunta. \n" \
        f"Puntos a considerar: \n" \
        f"1. Los análisis proporcionados deben guiarte hacia la respuesta correcta. \n" \
        f"2. Cualquier opción que contenga información incorrecta no puede ser la respuesta correcta. \n" \
        f"3. Por favor, responde solo con la letra de la opción seleccionada, como A, B, C, D o E, usando el siguiente formato: '''Option: [Letra de la Opción Seleccionada]'''. " \
        f"Recuerda, necesitamos solo la letra, no el contenido completo de la opción."

    return prompt


def get_final_answer_prompt_wsyn(syn_report):
    prompt = f"A continuación, se presenta un informe sintetizado: {syn_report} \n" \
        f"Con base en el informe anterior, selecciona la opción óptima para responder la pregunta. \n" \
        f"Puntos a considerar: \n" \
        f"1. Los análisis proporcionados deben guiarte hacia la respuesta correcta. \n" \
        f"2. Cualquier opción que contenga información incorrecta no puede ser la opción correcta. \n" \
        f"3. Por favor, responde solo con la letra de la opción seleccionada, como A, B, C, D o E, usando el siguiente formato: '''Option: [Letra de la Opción Seleccionada]'''. " \
        f"Recuerda, necesitamos solo la letra, no el contenido completo de la opción."
    return prompt

def get_direct_prompt(question, options):
    prompt = f"Pregunta: {question} \n" \
        f"Opciones: {options} \n" \
        f"Por favor, responde solo con la letra de la opción seleccionada, como A, B, C, D o E, usando el siguiente formato: '''Option: [Letra de la Opción Seleccionada]'''."
    return prompt

def get_cot_prompt(question, options):
    cot_format = f"Pensamiento: [los pensamientos paso a paso] \n" \
                f"Respuesta: [Letra de la Opción Seleccionada (como A, B, C, D o E)] \n"
    prompt = f"Pregunta: {question} \n" \
        f"Opciones: {options} \n" \
        f"Respuesta: Vamos a resolver esto paso a paso para asegurarnos de tener la respuesta correcta. " \
        f"Debes entregar el resultado exactamente en el siguiente formato: '''{cot_format}'''"
    return prompt



def get_synthesized_report_prompt(question_analyses, option_analyses):
    synthesizer = "Eres un tomador de decisiones médicas experto en resumir y sintetizar informes basados en la opinión de múltiples expertos de diferentes dominios."

    syn_report_format = f"Key Knowledge: [conocimiento clave extraído] \n" \
                        f"Total Analysis: [análisis sintetizado] \n"
    prompt = f"A continuación, se presentan algunos informes de diferentes expertos médicos de diversos dominios.\n"
    prompt += f"Debes completar los siguientes pasos:" \
              f"1. Considera cuidadosamente y de manera integral los siguientes informes." \
              f"2. Extrae el conocimiento clave de los informes proporcionados. " \
              f"3. Deriva un análisis comprensivo y resumido basado en el conocimiento." \
              f"4. Tu objetivo final es elaborar un informe refinado y sintetizado basado en los informes anteriores." \
              f"Debes entregar el resultado exactamente en el siguiente formato: '''{syn_report_format}'''"
    prompt += question_analyses
    prompt += option_analyses
    
    return synthesizer, prompt

def get_consensus_prompt(domain, syn_report):
    voter = f"Eres un experto médico especializado en el campo de {domain}."
    cons_prompt = f"A continuación, se presenta un informe médico: {syn_report} \n"\
        f"Como experto médico especializado en {domain}, por favor, lee detenidamente el informe y decide si tus opiniones son consistentes con este informe." \
        f"Por favor, responde solo con: [YES or NO]."
    return voter, cons_prompt



def get_consensus_opinion_prompt(domain, syn_report):
    opinion_prompt = f"A continuación, se presenta un informe médico: {syn_report} \n"\
        f"Como experto médico especializado en {domain}, utiliza plenamente tu experiencia para proponer revisiones a este informe." \
        f"Debes entregar el resultado exactamente en el siguiente formato: '''Revisions: [consejo de revisión propuesto] '''"
    return opinion_prompt



#revision_prompt = get_revision_prompt(revision_advice)

def get_revision_prompt(syn_report, revision_advice):
    revision_prompt = f"A continuación, se presenta el informe original: {syn_report}\n\n"
    for domain, advice in revision_advice.items():
        revision_prompt += f"Aquí tienes el consejo de un experto médico especializado en {domain}: {advice}.\n"
    revision_prompt += f"Con base en los consejos anteriores, entrega el análisis revisado en el siguiente formato: '''Total Analysis: [análisis revisado] '''"
    return revision_prompt
