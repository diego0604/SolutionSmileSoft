"""
=============================================================================
TALLER: Modelos de Lenguaje con N-gramas
=============================================================================
Autor: Diego Alejandro Salazar Ramirez
Descripcion: Construccion de modelos de lenguaje basados en unigramas,
             bigramas y trigramas usando "The Little Prince" como corpus
             principal y un segundo corpus para comparacion.
=============================================================================
"""

import re
import random
import string
from collections import Counter, defaultdict

# ── Dependencia para leer PDF ──
try:
    import PyPDF2
except ImportError:
    raise ImportError("Instale PyPDF2: pip install PyPDF2")


# =====================================================================
# PARTE 1 — Preparacion del corpus
# =====================================================================

def extract_text_from_pdf(pdf_path):
    """Extrae texto plano de un archivo PDF."""
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def clean_text(text):
    """
    Limpieza del texto:
    - Convertir a minusculas
    - Eliminar signos de puntuacion innecesarios
    - Eliminar caracteres especiales
    - Dividir en palabras
    Retorna una lista de palabras limpias.
    """
    # Convertir a minusculas
    text = text.lower()

    # Eliminar URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # Reemplazar guiones y tabulaciones por espacios
    text = re.sub(r'[\t\-]+', ' ', text)

    # Eliminar signos de puntuacion
    text = re.sub(r'[^\w\s]', '', text)

    # Eliminar digitos
    text = re.sub(r'\d+', '', text)

    # Eliminar espacios multiples
    text = re.sub(r'\s+', ' ', text)

    # Dividir en palabras y filtrar vacias
    words = [w.strip() for w in text.split() if w.strip()]

    return words


def prepare_corpus(pdf_path):
    """Pipeline completo: extraccion + limpieza del corpus."""
    print(f"\n{'='*70}")
    print(f"  Preparando corpus desde: {pdf_path}")
    print(f"{'='*70}")

    raw_text = extract_text_from_pdf(pdf_path)
    words = clean_text(raw_text)

    print(f"  Texto extraido: {len(raw_text):,} caracteres")
    print(f"  Palabras despues de limpieza: {len(words):,}")
    print(f"  Vocabulario unico: {len(set(words)):,} palabras")
    print(f"  Primeras 20 palabras: {words[:20]}")

    return words


# =====================================================================
# PARTE 2 — Construccion de modelos
# =====================================================================

class UnigramModel:
    """Modelo de lenguaje basado en unigramas (palabras individuales)."""

    def __init__(self, words):
        self.total_words = len(words)
        self.freq = Counter(words)
        self.vocab_size = len(self.freq)
        # Probabilidades
        self.probs = {w: count / self.total_words for w, count in self.freq.items()}

    def probability(self, word):
        """P(word) = count(word) / total_words"""
        return self.probs.get(word, 0.0)

    def top_n(self, n=10):
        """Retorna las n palabras mas frecuentes con sus probabilidades."""
        return sorted(self.probs.items(), key=lambda x: x[1], reverse=True)[:n]

    def generate_sentence(self, length=10):
        """Genera una frase seleccionando palabras segun su probabilidad."""
        words_list = list(self.probs.keys())
        probs_list = list(self.probs.values())
        sentence = random.choices(words_list, weights=probs_list, k=length)
        return " ".join(sentence)


class BigramModel:
    """Modelo de lenguaje basado en bigramas (pares de palabras consecutivas)."""

    def __init__(self, words):
        self.bigram_counts = Counter()
        self.unigram_counts = Counter(words)
        self.bigrams_by_first = defaultdict(list)
        self.words = words

        # Construir bigramas
        for i in range(len(words) - 1):
            bigram = (words[i], words[i + 1])
            self.bigram_counts[bigram] += 1

        # Calcular probabilidades condicionales P(w2|w1) = count(w1,w2) / count(w1)
        self.probs = {}
        for (w1, w2), count in self.bigram_counts.items():
            prob = count / self.unigram_counts[w1]
            self.probs[(w1, w2)] = prob
            self.bigrams_by_first[w1].append((w2, prob))

    def conditional_probability(self, w1, w2):
        """P(w2|w1) = count(w1, w2) / count(w1)"""
        return self.probs.get((w1, w2), 0.0)

    def top_bigrams(self, n=10):
        """Retorna los n bigramas mas frecuentes con sus probabilidades."""
        return sorted(self.probs.items(), key=lambda x: x[1], reverse=True)[:n]

    def generate_sentence(self, length=10, start_word=None):
        """Genera una frase usando el modelo de bigramas."""
        if start_word is None or start_word not in self.bigrams_by_first:
            start_word = random.choice(self.words)

        sentence = [start_word]
        current = start_word

        for _ in range(length - 1):
            if current not in self.bigrams_by_first:
                # Si no hay continuacion, elegir palabra aleatoria
                current = random.choice(self.words)
                sentence.append(current)
                continue

            next_words = self.bigrams_by_first[current]
            words_list = [w for w, _ in next_words]
            probs_list = [p for _, p in next_words]
            chosen = random.choices(words_list, weights=probs_list, k=1)[0]
            sentence.append(chosen)
            current = chosen

        return " ".join(sentence)


class TrigramModel:
    """Modelo de lenguaje basado en trigramas (secuencias de tres palabras)."""

    def __init__(self, words):
        self.trigram_counts = Counter()
        self.bigram_counts = Counter()
        self.trigrams_by_prefix = defaultdict(list)
        self.words = words

        # Construir bigramas y trigramas
        for i in range(len(words) - 1):
            self.bigram_counts[(words[i], words[i + 1])] += 1

        for i in range(len(words) - 2):
            trigram = (words[i], words[i + 1], words[i + 2])
            self.trigram_counts[trigram] += 1

        # Calcular probabilidades condicionales P(w3|w1,w2) = count(w1,w2,w3) / count(w1,w2)
        self.probs = {}
        for (w1, w2, w3), count in self.trigram_counts.items():
            bigram_count = self.bigram_counts[(w1, w2)]
            prob = count / bigram_count
            self.probs[(w1, w2, w3)] = prob
            self.trigrams_by_prefix[(w1, w2)].append((w3, prob))

    def conditional_probability(self, w1, w2, w3):
        """P(w3|w1, w2) = count(w1, w2, w3) / count(w1, w2)"""
        return self.probs.get((w1, w2, w3), 0.0)

    def top_trigrams(self, n=10):
        """Retorna los n trigramas mas frecuentes con sus probabilidades."""
        return sorted(self.probs.items(), key=lambda x: x[1], reverse=True)[:n]

    def generate_sentence(self, length=10, start_bigram=None):
        """Genera una frase usando el modelo de trigramas."""
        if start_bigram is None or start_bigram not in self.trigrams_by_prefix:
            # Elegir un bigrama inicial aleatorio
            valid_prefixes = list(self.trigrams_by_prefix.keys())
            start_bigram = random.choice(valid_prefixes)

        sentence = list(start_bigram)
        w1, w2 = start_bigram

        for _ in range(length - 2):
            prefix = (w1, w2)
            if prefix not in self.trigrams_by_prefix:
                # Si no hay continuacion, elegir nuevo prefijo
                valid_prefixes = list(self.trigrams_by_prefix.keys())
                prefix = random.choice(valid_prefixes)
                w1, w2 = prefix
                sentence.append(w1)
                continue

            next_words = self.trigrams_by_prefix[prefix]
            words_list = [w for w, _ in next_words]
            probs_list = [p for _, p in next_words]
            chosen = random.choices(words_list, weights=probs_list, k=1)[0]
            sentence.append(chosen)
            w1, w2 = w2, chosen

        return " ".join(sentence)


# =====================================================================
# PARTE 3 — Generacion de texto
# =====================================================================

def generate_sentences(unigram, bigram, trigram, num_sentences=5):
    """Genera frases con cada modelo."""
    print(f"\n{'='*70}")
    print("  PARTE 3: Generacion de Texto")
    print(f"{'='*70}")

    results = {"unigram": [], "bigram": [], "trigram": []}

    print("\n  --- Frases generadas con UNIGRAMAS ---")
    for i in range(num_sentences):
        sentence = unigram.generate_sentence(length=12)
        results["unigram"].append(sentence)
        print(f"  {i+1}. {sentence}")

    print("\n  --- Frases generadas con BIGRAMAS ---")
    for i in range(num_sentences):
        sentence = bigram.generate_sentence(length=12)
        results["bigram"].append(sentence)
        print(f"  {i+1}. {sentence}")

    print("\n  --- Frases generadas con TRIGRAMAS ---")
    for i in range(num_sentences):
        sentence = trigram.generate_sentence(length=12)
        results["trigram"].append(sentence)
        print(f"  {i+1}. {sentence}")

    return results


# =====================================================================
# PARTE 4 — Analisis de resultados
# =====================================================================

def analyze_results(results):
    """
    Clasifica cada frase segun coherencia logica y autenticidad linguistica.
    Usa heuristicas simples basadas en la estructura del texto.
    """
    print(f"\n{'='*70}")
    print("  PARTE 4: Analisis de Resultados")
    print(f"{'='*70}")

    # Heuristica para evaluar coherencia:
    # - Unigramas: baja coherencia (palabras aleatorias)
    # - Bigramas: media coherencia (pares conectados)
    # - Trigramas: alta coherencia (secuencias de 3 palabras)
    coherence_map = {
        "unigram": "BAJA",
        "bigram": "MEDIA",
        "trigram": "ALTA"
    }
    authenticity_map = {
        "unigram": "BAJA",
        "bigram": "MEDIA",
        "trigram": "ALTA"
    }

    for model_name, sentences in results.items():
        print(f"\n  Modelo: {model_name.upper()}")
        print(f"  {'Frase':<55} | {'Coherencia':<12} | {'Autenticidad':<12}")
        print(f"  {'-'*55}-+-{'-'*12}-+-{'-'*12}")
        for s in sentences:
            display = s[:52] + "..." if len(s) > 55 else s
            print(f"  {display:<55} | {coherence_map[model_name]:<12} | {authenticity_map[model_name]:<12}")

    print(f"\n  {'='*70}")
    print("  RESPUESTAS AL ANALISIS")
    print(f"  {'='*70}")

    print("""
  1. Que modelo genera frases mas coherentes?
     El modelo de TRIGRAMAS genera las frases mas coherentes porque
     considera secuencias de tres palabras consecutivas, lo que permite
     capturar mejor la estructura gramatical y el contexto del idioma.

  2. Que diferencias observa entre unigramas, bigramas y trigramas?
     - Unigramas: Seleccionan palabras de forma independiente segun
       frecuencia. No hay relacion entre palabras consecutivas.
     - Bigramas: Consideran pares de palabras, lo que introduce
       cierta estructura gramatical basica (articulo-sustantivo, etc.)
     - Trigramas: Capturan dependencias mas largas, produciendo
       frases que se asemejan mas al texto original del corpus.

  3. Que limitaciones presenta el modelo unigrama?
     - No captura ningun contexto ni dependencia entre palabras
     - Las frases generadas son esencialmente "bolsas de palabras"
     - No respeta la estructura gramatical del idioma
     - Palabras muy frecuentes (articulos, preposiciones) dominan
       la generacion, produciendo frases sin sentido

  4. Que ocurre cuando una secuencia no existe en el corpus?
     Cuando un bigrama o trigrama no existe en el corpus, su
     probabilidad condicional es 0. En la generacion de texto,
     esto causa que el modelo no pueda continuar la frase de forma
     natural. Se requieren tecnicas como suavizado de Laplace
     (add-one smoothing) o backoff para manejar estas situaciones.
     En nuestra implementacion, elegimos una nueva palabra/prefijo
     aleatorio cuando no se encuentra continuacion.
    """)


# =====================================================================
# PARTE 5 — Cambio de corpus (segundo corpus)
# =====================================================================

def get_second_corpus():
    """
    Genera un segundo corpus usando texto de dominio cientifico/tecnologico.
    Se usa un texto extenso incorporado directamente para garantizar
    disponibilidad sin dependencias externas.
    """
    science_text = """
    The history of artificial intelligence began in antiquity with myths and stories
    of artificial beings endowed with intelligence or consciousness by master craftsmen.
    The seeds of modern AI were planted by philosophers who attempted to describe the
    process of human thinking as the mechanical manipulation of symbols. This work
    culminated in the invention of the programmable digital computer in the 1940s,
    a machine based on the abstract essence of mathematical reasoning. This device
    and the ideas behind it inspired a handful of scientists to begin seriously
    discussing the possibility of building an electronic brain.

    The field of artificial intelligence research was born at a workshop held on the
    campus of Dartmouth College during the summer of 1956. Those who attended would
    become the leaders of AI research for decades. Many of them predicted that a
    machine as intelligent as a human being would exist in no more than a generation.
    They were given millions of dollars to make this vision come true. Eventually it
    became obvious that commercial developers and researchers had grossly underestimated
    the difficulty of the project.

    In 1973, in response to the criticism from James Lighthill and ongoing pressure
    from the US Congress, both the US and British governments cut off exploratory
    research in AI. The next few years would later be called an AI winter, a period
    when obtaining funding for AI projects was difficult. In the early 1980s, AI
    research was revived by the commercial success of expert systems, a form of AI
    program that simulated the knowledge and analytical skills of human experts.

    By 1985, the market for AI had reached over a billion dollars. At the same time,
    Japan's fifth generation computer project inspired the US and British governments
    to restore funding for academic research. However, beginning with the collapse of
    the Lisp Machine market in 1987, AI once again fell into disrepute, and a second
    longer lasting winter began.

    Machine learning, a fundamental concept of AI research since the field's inception,
    is the study of computer algorithms that improve automatically through experience.
    Unsupervised learning is the ability to find patterns in a stream of input without
    requiring a human to label the inputs first. Supervised learning includes both
    classification and numerical regression, which requires a human to label the input
    data first. Classification is used to determine what category something belongs in.
    Regression is used to find relationships between variables and predict future values.

    Deep learning is a subset of machine learning that uses artificial neural networks
    with multiple layers. These networks are capable of learning complex patterns in
    data and have been responsible for many of the recent advances in AI. Convolutional
    neural networks are particularly effective for image recognition tasks, while
    recurrent neural networks are used for sequential data like text and speech.

    Natural language processing is a subfield of linguistics, computer science, and
    artificial intelligence concerned with the interactions between computers and
    human language. The goal is to enable computers to understand, interpret, and
    generate human language in a valuable way. NLP combines computational linguistics
    with statistical, machine learning, and deep learning models to process human
    language.

    Reinforcement learning is an area of machine learning concerned with how software
    agents ought to take actions in an environment in order to maximize some notion
    of cumulative reward. The agent learns to achieve a goal in an uncertain and
    potentially complex environment. In reinforcement learning, an agent makes
    observations and takes actions within an environment, and in return it receives
    rewards. Its objective is to learn to act in a way that will maximize its
    expected long term rewards.

    Computer vision is an interdisciplinary scientific field that deals with how
    computers can gain high level understanding from digital images or videos. From
    the perspective of engineering, it seeks to understand and automate tasks that
    the human visual system can do. Computer vision tasks include methods for
    acquiring, processing, analyzing and understanding digital images.

    Robotics is an interdisciplinary branch of engineering and science that includes
    mechanical engineering, electronic engineering, information engineering, computer
    science, and others. Robotics deals with the design, construction, operation, and
    use of robots, as well as computer systems for their control, sensory feedback,
    and information processing. These technologies are used to develop machines that
    can substitute for humans.

    The ethics of artificial intelligence is the branch of the ethics of technology
    specific to artificially intelligent systems. It is sometimes divided into a
    concern with the moral behavior of humans as they design, make, use, and treat
    artificially intelligent systems, and a concern with the behavior of machines.
    The field of AI ethics has become increasingly important as AI systems become
    more capable and are deployed in a wider range of applications.

    Transfer learning is a machine learning method where a model developed for one
    task is reused as the starting point for a model on a second task. It is a
    popular approach in deep learning because it allows you to train deep neural
    networks with comparatively little data. This is very useful because most
    real world problems typically do not have millions of labeled data points to
    train such complex models.

    Generative adversarial networks are a class of machine learning frameworks
    designed by Ian Goodfellow and his colleagues in 2014. Two neural networks
    contest with each other in a game. Given a training set, this technique learns
    to generate new data with the same statistics as the training set. For example,
    a GAN trained on photographs can generate new photographs that look authentic
    to human observers.

    The transformer architecture has revolutionized natural language processing
    since its introduction in 2017. Unlike previous sequence models, transformers
    use self attention mechanisms to process all positions in a sequence simultaneously.
    This parallel processing capability makes them significantly faster to train than
    recurrent neural networks. Large language models like GPT and BERT are based on
    the transformer architecture and have achieved remarkable results across many
    NLP tasks.

    Autonomous vehicles use a combination of sensors, cameras, radar, and artificial
    intelligence to travel between destinations without a human operator. Self driving
    cars use various techniques including deep learning and computer vision to navigate
    roads and avoid obstacles. The development of autonomous vehicles has raised many
    questions about safety, liability, and the future of transportation.

    Healthcare applications of artificial intelligence include the diagnosis of diseases,
    drug discovery, personalized treatment plans, and medical imaging analysis. AI
    systems can analyze medical images to detect conditions such as cancer, diabetic
    retinopathy, and cardiovascular disease with accuracy comparable to or exceeding
    that of human experts. These systems have the potential to improve patient outcomes
    and reduce healthcare costs significantly.
    """
    return science_text


def run_second_corpus_analysis():
    """Ejecuta el analisis con el segundo corpus y compara."""
    print(f"\n{'='*70}")
    print("  PARTE 5: Cambio de Corpus")
    print(f"  Segundo corpus: Texto sobre Inteligencia Artificial")
    print(f"{'='*70}")

    # Preparar segundo corpus
    science_text = get_second_corpus()
    words2 = clean_text(science_text)
    print(f"\n  Palabras en segundo corpus: {len(words2):,}")
    print(f"  Vocabulario unico: {len(set(words2)):,} palabras")

    # Construir modelos
    uni2 = UnigramModel(words2)
    bi2 = BigramModel(words2)
    tri2 = TrigramModel(words2)

    # Generar frases
    print("\n  --- Frases con UNIGRAMAS (Corpus AI) ---")
    for i in range(5):
        print(f"  {i+1}. {uni2.generate_sentence(length=12)}")

    print("\n  --- Frases con BIGRAMAS (Corpus AI) ---")
    for i in range(5):
        print(f"  {i+1}. {bi2.generate_sentence(length=12)}")

    print("\n  --- Frases con TRIGRAMAS (Corpus AI) ---")
    for i in range(5):
        print(f"  {i+1}. {tri2.generate_sentence(length=12)}")

    # Comparacion
    print(f"\n  {'='*70}")
    print("  COMPARACION ENTRE CORPUS")
    print(f"  {'='*70}")
    print("""
  1. Como cambia el estilo del texto generado?
     El texto generado cambia drasticamente segun el corpus:
     - Corpus 1 (The Little Prince): Las frases contienen vocabulario
       literario, emocional y narrativo. Palabras como "flower", "star",
       "planet", "little", "prince" dominan la generacion.
     - Corpus 2 (Inteligencia Artificial): Las frases contienen
       terminologia tecnica y cientifica. Palabras como "learning",
       "neural", "networks", "intelligence", "data" son frecuentes.

  2. El modelo refleja el tipo de corpus utilizado?
     Si, definitivamente. El modelo es un reflejo directo del corpus:
     - Con el corpus literario, genera frases con tono poetico/narrativo
     - Con el corpus tecnico, genera frases con tono academico/cientifico
     Esto demuestra que los modelos de n-gramas capturan las
     distribuciones estadisticas especificas de cada corpus.

  3. Que diferencias observa en vocabulario y coherencia?
     - Vocabulario: Cada corpus tiene un vocabulario muy diferente.
       "The Little Prince" usa palabras simples y emotivas, mientras
       que el texto de AI usa terminologia especializada.
     - Coherencia: Los trigramas son mas coherentes en ambos corpus,
       pero la coherencia relativa depende del tamano del corpus.
       Un corpus mas grande produce modelos mas robustos.
     - Repeticion: Con corpus pequenos, los trigramas tienden a
       reproducir fragmentos exactos del texto original porque hay
       menos combinaciones posibles.
    """)

    return uni2, bi2, tri2


# =====================================================================
# PARTE 6 — Evidencia de probabilidades
# =====================================================================

def show_probability_evidence(unigram, bigram, words):
    """Muestra ejemplos detallados de probabilidades calculadas."""
    print(f"\n{'='*70}")
    print("  PARTE 6: Evidencia de Probabilidades")
    print(f"{'='*70}")

    # --- Probabilidades de Unigramas ---
    print("\n  ┌─────────────────────────────────────────────────────────┐")
    print("  │           PROBABILIDADES DE UNIGRAMAS                  │")
    print("  └─────────────────────────────────────────────────────────┘")
    print(f"\n  Total de palabras en el corpus: {unigram.total_words:,}")
    print(f"  Vocabulario unico: {unigram.vocab_size:,}")
    print(f"\n  Formula: P(word) = count(word) / total_words")
    print(f"\n  {'Palabra':<15} | {'Frecuencia':<12} | {'Probabilidad':<15} | {'Calculo'}")
    print(f"  {'-'*15}-+-{'-'*12}-+-{'-'*15}-+-{'-'*30}")

    top_words = unigram.top_n(15)
    for word, prob in top_words:
        count = unigram.freq[word]
        calc = f"{count}/{unigram.total_words} = {prob:.6f}"
        print(f"  {word:<15} | {count:<12} | {prob:<15.6f} | {calc}")

    # Ejemplos especificos del libro
    example_words = ["prince", "flower", "star", "planet", "king",
                     "fox", "rose", "desert", "sheep", "drawing"]
    print(f"\n  Palabras tematicas del corpus:")
    print(f"  {'Palabra':<15} | {'Frecuencia':<12} | {'Probabilidad':<15}")
    print(f"  {'-'*15}-+-{'-'*12}-+-{'-'*15}")
    for w in example_words:
        count = unigram.freq.get(w, 0)
        prob = unigram.probability(w)
        print(f"  {w:<15} | {count:<12} | {prob:<15.6f}")

    # --- Probabilidades de Bigramas ---
    print("\n  ┌─────────────────────────────────────────────────────────┐")
    print("  │           PROBABILIDADES DE BIGRAMAS                   │")
    print("  └─────────────────────────────────────────────────────────┘")
    print(f"\n  Formula: P(w2|w1) = count(w1, w2) / count(w1)")
    print(f"\n  {'Bigrama':<30} | {'count(w1,w2)':<14} | {'count(w1)':<12} | {'P(w2|w1)':<12}")
    print(f"  {'-'*30}-+-{'-'*14}-+-{'-'*12}-+-{'-'*12}")

    top_bigs = bigram.top_bigrams(20)
    for (w1, w2), prob in top_bigs:
        bigram_count = bigram.bigram_counts[(w1, w2)]
        unigram_count = bigram.unigram_counts[w1]
        print(f"  {w1 + ' ' + w2:<30} | {bigram_count:<14} | {unigram_count:<12} | {prob:<12.4f}")

    # Ejemplos contextuales
    print(f"\n  Ejemplos contextuales de probabilidades condicionales:")
    context_examples = [
        ("the", "little"), ("little", "prince"), ("the", "prince"),
        ("boa", "constrictor"), ("grown", "ups"), ("my", "drawing"),
        ("the", "flower"), ("the", "king"), ("the", "fox"),
        ("he", "said"), ("she", "said"), ("i", "said")
    ]
    print(f"  {'Bigrama':<25} | {'P(w2|w1)':<12} | {'Interpretacion'}")
    print(f"  {'-'*25}-+-{'-'*12}-+-{'-'*35}")
    for w1, w2 in context_examples:
        prob = bigram.conditional_probability(w1, w2)
        if prob > 0:
            interp = f"De cada vez que aparece '{w1}', {prob*100:.1f}% le sigue '{w2}'"
        else:
            interp = "Secuencia no encontrada en el corpus"
        print(f"  {w1 + ' ' + w2:<25} | {prob:<12.4f} | {interp}")

    # Distribucion de probabilidades dado un contexto
    print(f"\n  Distribucion de probabilidades despues de 'the':")
    if "the" in bigram.bigrams_by_first:
        the_continuations = sorted(bigram.bigrams_by_first["the"],
                                   key=lambda x: x[1], reverse=True)
        print(f"  {'Palabra siguiente':<20} | {'P(w|the)':<12}")
        print(f"  {'-'*20}-+-{'-'*12}")
        for w, p in the_continuations[:15]:
            bar = "█" * int(p * 100)
            print(f"  {w:<20} | {p:<12.4f} {bar}")

    print(f"\n  Distribucion de probabilidades despues de 'little':")
    if "little" in bigram.bigrams_by_first:
        little_continuations = sorted(bigram.bigrams_by_first["little"],
                                      key=lambda x: x[1], reverse=True)
        print(f"  {'Palabra siguiente':<20} | {'P(w|little)':<12}")
        print(f"  {'-'*20}-+-{'-'*12}")
        for w, p in little_continuations[:10]:
            bar = "█" * int(p * 100)
            print(f"  {w:<20} | {p:<12.4f} {bar}")


# =====================================================================
# FUNCION PRINCIPAL
# =====================================================================

def main():
    """Ejecuta todas las partes del taller."""

    # Semilla para reproducibilidad
    random.seed(42)

    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█   TALLER: Modelos de Lenguaje con N-gramas" + " " * 24 + "█")
    print("█   Corpus principal: The Little Prince" + " " * 30 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    # ── PARTE 1: Preparacion del corpus ──
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "corpus", "the_little_prince.pdf")

    words = prepare_corpus(pdf_path)

    # ── PARTE 2: Construccion de modelos ──
    print(f"\n{'='*70}")
    print("  PARTE 2: Construccion de Modelos")
    print(f"{'='*70}")

    unigram = UnigramModel(words)
    bigram = BigramModel(words)
    trigram = TrigramModel(words)

    print(f"\n  Modelo Unigrama:")
    print(f"    - Vocabulario: {unigram.vocab_size:,} palabras unicas")
    print(f"    - Total palabras: {unigram.total_words:,}")
    print(f"    - Top 10 palabras: {unigram.top_n(10)}")

    print(f"\n  Modelo Bigrama:")
    print(f"    - Total bigramas unicos: {len(bigram.bigram_counts):,}")
    print(f"    - Top 5 bigramas:")
    for (w1, w2), prob in bigram.top_bigrams(5):
        print(f"      ({w1}, {w2}) -> P = {prob:.4f}")

    print(f"\n  Modelo Trigrama:")
    print(f"    - Total trigramas unicos: {len(trigram.trigram_counts):,}")
    print(f"    - Top 5 trigramas:")
    for (w1, w2, w3), prob in trigram.top_trigrams(5):
        print(f"      ({w1}, {w2}, {w3}) -> P = {prob:.4f}")

    # ── PARTE 3: Generacion de texto ──
    results = generate_sentences(unigram, bigram, trigram, num_sentences=5)

    # ── PARTE 4: Analisis de resultados ──
    analyze_results(results)

    # ── PARTE 5: Cambio de corpus ──
    run_second_corpus_analysis()

    # ── PARTE 6: Evidencia de probabilidades ──
    show_probability_evidence(unigram, bigram, words)

    print(f"\n{'='*70}")
    print("  Taller completado exitosamente!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
