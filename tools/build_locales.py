"""Generate /es, /cy and /mt from the English index.html.

Run from the repository root:  python3 tools/build_locales.py

Every English string is replaced explicitly; the script fails if a source
string is missing, so the English template and the translations cannot drift
silently. After changing English copy, update COMMON_EN and each locale here,
then re-run.
"""
import json
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

COMMON_EN = {
    "title": "<title>reBottled | Great water at home, without plastic bottles</title>",
    "desc": '<meta name="description" content="reBottled is a social enterprise bringing clean, great-tasting tap water to homes in Malta, Cyprus and the Canary Islands, so families can stop buying water in plastic.">',
    "ogtitle": '<meta property="og:title" content="reBottled | Great water at home, without plastic bottles">',
    "ogdesc": '<meta property="og:description" content="A home water system on subscription for Malta, Cyprus and the Canary Islands. Join the pilot: first month and installation free.">',
    "skip": '>Skip to content</a>',
    "brand": 'aria-label="reBottled, back to top"',
    "note": '<p class="header-note">Pilot opening in <span>Malta, Cyprus and the Canary Islands</span></p>',
    "h1": '<span class="hero-title-line">Tap water that tastes like bottled.</span> <span class="hero-title-line hero-title-quiet">Minus the plastic.</span>',
    "lead": '<p class="hero-lead">A home filter on subscription. Pilot homes get the first month and installation free.</p>',
    "alt": 'alt="The reBottled filter: a slim white cylinder with a brushed metal end cap and the green reBottled logo"',
    "label": '>Email address</label>',
    "placeholder": 'placeholder="Your email address"',
    "button": '>Notify me</button>',
    "fieldnote": '<p class="signup-note">News about the pilot only. Unsubscribe any time.</p>',
    "impact_h2": '>Every glass is a bottle that never gets made.</h2>',
    "impact_lead": '<p class="lead">We are a social enterprise. We count our success in profit and in plastic bottles our customers no longer buy, and every home gets a yearly bottle report.</p>',
    "chart_title": '>Bottled water per person each year, in 1.5 L bottles</p>',
    "row_mt": '<div class="bar-row">\n                <dt>Malta</dt>',
    "row_cy": '<div class="bar-row">\n                <dt>Cyprus</dt>',
    "row_es": '<div class="bar-row">\n                <dt>Canary Islands</dt>',
    "row_eu": '<dt>EU average</dt>',
    "grid": '<div class="bottle-grid" role="img" aria-label="A grid of 450 small plastic bottles"></div>',
    "caption": '<figcaption><span class="wall-number">450</span> bottles a typical Maltese home stops buying every year.</figcaption>',
    "compare_h2": '>Better for the islands, easier for you</h2>',
    "compare_aria": 'aria-label="Bottled water compared with reBottled"',
    "compared_on": '>Compared on</span>',
    "head_bottled": '</svg>Bottled water</span>',
    "data_bottled": 'data-label="Bottled"',
    "r1h": '>Plastic bottles a year</span>',
    "r1b": '<span>About 450 per home</span>',
    "r1u": '<span><strong>None</strong></span>',
    "r2h": '>Carrying</span>',
    "r2b": '<span>Packs from the shop, every week</span>',
    "r2u": '<span><strong>Nothing.</strong> It comes from your tap</span>',
    "r3h": '>Taste</span>',
    "r3b": '<span>Depends on the brand</span>',
    "r3u": '<span><strong>No salt, no chlorine,</strong> minerals added back</span>',
    "r4h": '>Cost in Malta</span>',
    "r4b": '<span>About €17–30 a month</span>',
    "r4u": '<span><strong>€24.90</strong> a month, all in</span>',
    "how_h2": '>Simple to start, simple to stop</h2>',
    "s1h": '<h3>We send the system</h3>',
    "s1p": '<p>A compact unit for under the sink, with its own small tap.</p>',
    "s2h": '<h3>Fitted in 30 minutes</h3>',
    "s2p": '<p>Do it yourself with our video. Free installation for pilot homes.</p>',
    "s3h": '<h3>Filters arrive on time</h3>',
    "s3p": '<p>They twist in without tools. Leave any time and we take it back.</p>',
    "price": '<span class="price-amount">€24.90</span><span class="price-unit">a month, everything included</span>',
    "c1": '</svg>System on loan</li>',
    "c2": '</svg>All filters</li>',
    "c3": '</svg>Support</li>',
    "c4": '</svg>Yearly bottle report</li>',
    "pricefine": '<p class="fine price-fine">24-month plan. Pilot homes get the first month and installation free.</p>',
    "join_h2": '>Be first when we reach your island.</h2>',
    "join_lead": '<p class="join-lead">The pilot starts in Malta, then Cyprus and the Canary Islands. Early sign-ups get the first month and installation free.</p>',
    "footer": '<p class="footer-line">Drink the tap, <span class="accent">skip the plastic.</span></p>',
    "copyright": 'reBottled. A social enterprise.</p>',
    "langnav": 'aria-label="Language"',
}

# Strings that appear more than once in the English page
REPEATS = {"label": 2, "placeholder": 2, "button": 2, "fieldnote": 2, "data_bottled": 4}

LOCALES = {
    "es": {
        "lang": "es",
        "fonts": None,
        "grid": {"n": 240, "cols": 20, "rows": 12, "mcols": 40, "mrows": 6},
        "local_row": "row_es",
        "t": {
            "title": "<title>reBottled | Agua del grifo que sabe a embotellada, sin plástico</title>",
            "desc": '<meta name="description" content="reBottled es una empresa social que lleva a los hogares de Canarias agua del grifo con buen sabor, para dejar de comprar agua en garrafas y botellas de plástico.">',
            "ogtitle": '<meta property="og:title" content="reBottled | Agua del grifo que sabe a embotellada, sin plástico">',
            "ogdesc": '<meta property="og:description" content="Un filtro para casa por suscripción en Canarias. Únete al piloto: primer mes e instalación gratis.">',
            "skip": '>Saltar al contenido</a>',
            "brand": 'aria-label="reBottled, volver arriba"',
            "note": '<p class="header-note">Piloto muy pronto en <span>Canarias</span></p>',
            "h1": '<span class="hero-title-line">Agua del grifo que sabe a embotellada.</span> <span class="hero-title-line hero-title-quiet">Sin el plástico.</span>',
            "lead": '<p class="hero-lead">Un filtro para casa por suscripción. Los hogares del piloto tienen el primer mes y la instalación gratis.</p>',
            "alt": 'alt="El filtro reBottled: un cilindro blanco y estilizado con una tapa de metal cepillado y el logotipo verde de reBottled"',
            "label": '>Correo electrónico</label>',
            "placeholder": 'placeholder="Tu correo electrónico"',
            "button": '>Avísame</button>',
            "fieldnote": '<p class="signup-note">Solo noticias sobre el piloto. Puedes darte de baja cuando quieras.</p>',
            "impact_h2": '>Cada vaso es una botella que nunca se fabrica.</h2>',
            "impact_lead": '<p class="lead">Somos una empresa social. Medimos nuestro éxito en beneficios y en las botellas de plástico que nuestros clientes dejan de comprar, y cada hogar recibe un informe anual de botellas.</p>',
            "chart_title": '>Agua embotellada por persona al año, en botellas de 1,5 L</p>',
            "row_mt": '<div class="bar-row">\n                <dt>Malta</dt>',
            "row_cy": '<div class="bar-row">\n                <dt>Chipre</dt>',
            "row_es": '<div class="bar-row is-local">\n                <dt>Canarias</dt>',
            "row_eu": '<dt>Media de la UE</dt>',
            "caption": '<figcaption><span class="wall-number">240</span> botellas al año que deja de comprar un hogar canario típico.</figcaption>',
            "grid_aria": "Una cuadrícula de 240 botellas de plástico pequeñas",
            "compare_h2": '>Mejor para las islas, más fácil para ti</h2>',
            "compare_aria": 'aria-label="Agua embotellada comparada con reBottled"',
            "compared_on": '>Comparamos</span>',
            "head_bottled": '</svg>Agua embotellada</span>',
            "data_bottled": 'data-label="Embotellada"',
            "r1h": '>Botellas de plástico al año</span>',
            "r1b": '<span>Unas 240 por hogar</span>',
            "r1u": '<span><strong>Ninguna</strong></span>',
            "r2h": '>Cargar con el agua</span>',
            "r2b": '<span>Garrafas del súper, cada semana</span>',
            "r2u": '<span><strong>Nada.</strong> Sale de tu grifo</span>',
            "r3h": '>Sabor</span>',
            "r3b": '<span>Depende de la marca</span>',
            "r3u": '<span><strong>Sin sal ni cloro,</strong> con minerales añadidos</span>',
            "r4h": '>En casa</span>',
            "r4b": '<span>Garrafas ocupando espacio</span>',
            "r4u": '<span><strong>Un equipo compacto</strong> bajo el fregadero</span>',
            "how_h2": '>Fácil de empezar, fácil de dejar</h2>',
            "s1h": '<h3>Te enviamos el equipo</h3>',
            "s1p": '<p>Un equipo compacto para debajo del fregadero, con su propio grifo.</p>',
            "s2h": '<h3>Instalado en 30 minutos</h3>',
            "s2p": '<p>Hazlo tú con nuestro vídeo. Instalación gratis en los hogares del piloto.</p>',
            "s3h": '<h3>Filtros siempre a tiempo</h3>',
            "s3p": '<p>Se cambian con un giro, sin herramientas. Si te vas, nos llevamos el equipo.</p>',
            "price": '<span class="price-amount">24,90 €</span><span class="price-unit">al mes, todo incluido</span>',
            "c1": '</svg>Equipo en préstamo</li>',
            "c2": '</svg>Todos los filtros</li>',
            "c3": '</svg>Asistencia</li>',
            "c4": '</svg>Informe anual de botellas</li>',
            "pricefine": '<p class="fine price-fine">Plan de 24 meses. Los hogares del piloto tienen el primer mes y la instalación gratis.</p>',
            "join_h2": '>Sé de los primeros cuando lleguemos a Canarias.</h2>',
            "join_lead": '<p class="join-lead">El piloto empieza en Malta y después llegará a Canarias y Chipre. Si te apuntas pronto, el primer mes y la instalación son gratis.</p>',
            "footer": '<p class="footer-line">Bebe del grifo, <span class="accent">olvida el plástico.</span></p>',
            "copyright": 'reBottled. Una empresa social.</p>',
            "langnav": 'aria-label="Idioma"',
        },
        "js": {
            "sending": "Enviando…",
            "notify": "Avísame",
            "errorEmpty": "Escribe tu correo electrónico.",
            "errorInvalid": "Parece que ese correo no es válido. Revísalo, por favor.",
            "errorFailed": "Algo ha fallado y no hemos podido guardar tu correo. Inténtalo de nuevo.",
            "thanksTitle": "Ya estás en la lista.",
            "thanksQuestion": "Una cosa más: ¿dónde vives? Te avisaremos cuando el piloto llegue a tu zona.",
            "thanksPlace": "Te escribiremos en cuanto el piloto abra {place}, con el primer mes y la instalación gratis.",
            "thanksOther": "Te mantendremos al tanto y, si llegamos a tu zona, el primer mes y la instalación serán gratis.",
            "regions": [
                {"id": "canary-islands", "label": "Canarias", "place": "en Canarias"},
                {"id": "malta", "label": "Malta", "place": "en Malta"},
                {"id": "cyprus", "label": "Chipre", "place": "en Chipre"},
                {"id": "other", "label": "Otro lugar", "place": None},
            ],
        },
    },
    "cy": {
        "lang": "el",
        "fonts": "https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,300;7..72,400;7..72,500&family=Noto+Sans:wght@400;500;600&display=swap",
        "grid": {"n": 390, "cols": 26, "rows": 15, "mcols": 39, "mrows": 10},
        "local_row": "row_cy",
        "t": {
            "title": "<title>reBottled | Νερό βρύσης με γεύση εμφιαλωμένου, χωρίς πλαστικό</title>",
            "desc": '<meta name="description" content="Η reBottled είναι κοινωνική επιχείρηση που φέρνει στα σπίτια της Κύπρου νερό βρύσης με καλή γεύση, ώστε να μην αγοράζετε πια νερό σε πλαστικά μπουκάλια.">',
            "ogtitle": '<meta property="og:title" content="reBottled | Νερό βρύσης με γεύση εμφιαλωμένου, χωρίς πλαστικό">',
            "ogdesc": '<meta property="og:description" content="Φίλτρο νερού για το σπίτι με συνδρομή στην Κύπρο. Πιλοτικό πρόγραμμα: πρώτος μήνας και εγκατάσταση δωρεάν.">',
            "skip": '>Μετάβαση στο περιεχόμενο</a>',
            "brand": 'aria-label="reBottled, επιστροφή στην αρχή"',
            "note": '<p class="header-note">Πιλοτικό πρόγραμμα σύντομα στην <span>Κύπρο</span></p>',
            "h1": '<span class="hero-title-line">Νερό βρύσης με γεύση εμφιαλωμένου.</span> <span class="hero-title-line hero-title-quiet">Χωρίς το πλαστικό.</span>',
            "lead": '<p class="hero-lead">Ένα φίλτρο για το σπίτι με συνδρομή. Στα σπίτια του πιλοτικού προγράμματος ο πρώτος μήνας και η εγκατάσταση είναι δωρεάν.</p>',
            "alt": 'alt="Το φίλτρο reBottled: ένας λεπτός λευκός κύλινδρος με μεταλλικό καπάκι και το πράσινο λογότυπο της reBottled"',
            "label": '>Διεύθυνση email</label>',
            "placeholder": 'placeholder="Το email σας"',
            "button": '>Ενημερώστε με</button>',
            "fieldnote": '<p class="signup-note">Μόνο νέα για το πιλοτικό πρόγραμμα. Διαγραφή όποτε θέλετε.</p>',
            "impact_h2": '>Κάθε ποτήρι είναι ένα μπουκάλι που δεν θα φτιαχτεί ποτέ.</h2>',
            "impact_lead": '<p class="lead">Είμαστε κοινωνική επιχείρηση. Μετράμε την επιτυχία μας σε κέρδος και σε πλαστικά μπουκάλια που οι πελάτες μας δεν αγοράζουν πια, και κάθε σπίτι λαμβάνει μια ετήσια αναφορά μπουκαλιών.</p>',
            "chart_title": '>Εμφιαλωμένο νερό ανά άτομο τον χρόνο, σε μπουκάλια 1,5 λίτρου</p>',
            "row_mt": '<div class="bar-row">\n                <dt>Μάλτα</dt>',
            "row_cy": '<div class="bar-row is-local">\n                <dt>Κύπρος</dt>',
            "row_es": '<div class="bar-row">\n                <dt>Κανάριοι Νήσοι</dt>',
            "row_eu": '<dt>Μέσος όρος ΕΕ</dt>',
            "caption": '<figcaption><span class="wall-number">390</span> μπουκάλια τον χρόνο που ένα τυπικό κυπριακό σπίτι σταματά να αγοράζει.</figcaption>',
            "grid_aria": "Πλέγμα με 390 μικρά πλαστικά μπουκάλια",
            "compare_h2": '>Καλύτερο για το νησί, πιο εύκολο για εσάς</h2>',
            "compare_aria": 'aria-label="Εμφιαλωμένο νερό σε σύγκριση με το reBottled"',
            "compared_on": '>Σύγκριση</span>',
            "head_bottled": '</svg>Εμφιαλωμένο νερό</span>',
            "data_bottled": 'data-label="Εμφιαλωμένο"',
            "r1h": '>Πλαστικά μπουκάλια τον χρόνο</span>',
            "r1b": '<span>Περίπου 390 ανά σπίτι</span>',
            "r1u": '<span><strong>Κανένα</strong></span>',
            "r2h": '>Κουβάλημα</span>',
            "r2b": '<span>Μπουκάλια και ντεμιτζάνες, κάθε εβδομάδα</span>',
            "r2u": '<span><strong>Τίποτα.</strong> Τρέχει από τη βρύση σας</span>',
            "r3h": '>Γεύση</span>',
            "r3b": '<span>Εξαρτάται από τη μάρκα</span>',
            "r3u": '<span><strong>Χωρίς αλάτι και χλώριο,</strong> με πρόσθετα μέταλλα</span>',
            "r4h": '>Στο σπίτι</span>',
            "r4b": '<span>Ντεμιτζάνες που πιάνουν χώρο</span>',
            "r4u": '<span><strong>Μια μικρή συσκευή</strong> κάτω από τον νεροχύτη</span>',
            "how_h2": '>Εύκολο να ξεκινήσετε, εύκολο να σταματήσετε</h2>',
            "s1h": '<h3>Σας στέλνουμε τη συσκευή</h3>',
            "s1p": '<p>Μια μικρή μονάδα κάτω από τον νεροχύτη, με δική της βρυσούλα.</p>',
            "s2h": '<h3>Εγκατάσταση σε 30 λεπτά</h3>',
            "s2p": '<p>Μόνοι σας με το βίντεό μας. Δωρεάν εγκατάσταση για τα σπίτια του πιλοτικού.</p>',
            "s3h": '<h3>Φίλτρα στην ώρα τους</h3>',
            "s3p": '<p>Αλλάζουν με ένα στρίψιμο, χωρίς εργαλεία. Αν σταματήσετε, παίρνουμε πίσω τη συσκευή.</p>',
            "price": '<span class="price-amount">24,90 €</span><span class="price-unit">τον μήνα, όλα περιλαμβάνονται</span>',
            "c1": '</svg>Συσκευή με δανεισμό</li>',
            "c2": '</svg>Όλα τα φίλτρα</li>',
            "c3": '</svg>Υποστήριξη</li>',
            "c4": '</svg>Ετήσια αναφορά μπουκαλιών</li>',
            "pricefine": '<p class="fine price-fine">Πρόγραμμα 24 μηνών. Στα σπίτια του πιλοτικού ο πρώτος μήνας και η εγκατάσταση είναι δωρεάν.</p>',
            "join_h2": '>Μάθετε πρώτοι πότε ερχόμαστε στην Κύπρο.</h2>',
            "join_lead": '<p class="join-lead">Το πιλοτικό ξεκινά στη Μάλτα και στη συνέχεια έρχεται στην Κύπρο και στις Κανάριες Νήσους. Όσοι εγγραφούν νωρίς έχουν τον πρώτο μήνα και την εγκατάσταση δωρεάν.</p>',
            "footer": '<p class="footer-line">Πιείτε από τη βρύση, <span class="accent">αφήστε το πλαστικό.</span></p>',
            "copyright": 'reBottled. Μια κοινωνική επιχείρηση.</p>',
            "langnav": 'aria-label="Γλώσσα"',
        },
        "js": {
            "sending": "Αποστολή…",
            "notify": "Ενημερώστε με",
            "errorEmpty": "Γράψτε τη διεύθυνση email σας.",
            "errorInvalid": "Η διεύθυνση email δεν φαίνεται σωστή. Ελέγξτε την ξανά.",
            "errorFailed": "Κάτι πήγε στραβά και δεν αποθηκεύσαμε το email σας. Δοκιμάστε ξανά.",
            "thanksTitle": "Είστε στη λίστα.",
            "thanksQuestion": "Κάτι ακόμα: πού μένετε; Θα σας ενημερώσουμε όταν το πιλοτικό έρθει κοντά σας.",
            "thanksPlace": "Θα σας στείλουμε email μόλις ξεκινήσει το πιλοτικό {place}, με τον πρώτο μήνα και την εγκατάσταση δωρεάν.",
            "thanksOther": "Θα σας κρατάμε ενήμερους και, αν έρθουμε στην περιοχή σας, ο πρώτος μήνας και η εγκατάσταση θα είναι δωρεάν.",
            "regions": [
                {"id": "cyprus", "label": "Κύπρος", "place": "στην Κύπρο"},
                {"id": "malta", "label": "Μάλτα", "place": "στη Μάλτα"},
                {"id": "canary-islands", "label": "Κανάριοι Νήσοι", "place": "στις Κανάριες Νήσους"},
                {"id": "other", "label": "Κάπου αλλού", "place": None},
            ],
        },
    },
    "mt": {
        "lang": "mt",
        "fonts": None,
        "grid": None,  # same 450 as the English page
        "local_row": "row_mt",
        "t": {
            "title": "<title>reBottled | Ilma tal-vit b'togħma tal-ilma tal-flixkun, mingħajr plastik</title>",
            "desc": '<meta name="description" content="reBottled hija intrapriża soċjali li ġġib ilma tal-vit b\'togħma tajba fid-djar f\'Malta u Għawdex, biex ma jkollokx għalfejn tixtri l-ilma fi fliexken tal-plastik.">',
            "ogtitle": '<meta property="og:title" content="reBottled | Ilma tal-vit b\'togħma tal-ilma tal-flixkun, mingħajr plastik">',
            "ogdesc": '<meta property="og:description" content="Filtru tal-ilma għad-dar b\'abbonament f\'Malta. Ingħaqad mal-proġett pilota: l-ewwel xahar u l-installazzjoni b\'xejn.">',
            "skip": '>Aqbeż għall-kontenut</a>',
            "brand": 'aria-label="reBottled, lura fil-quċċata"',
            "note": '<p class="header-note">Il-proġett pilota jibda <span>f\'Malta</span></p>',
            "h1": '<span class="hero-title-line">Ilma tal-vit b\'togħma tal-ilma tal-flixkun.</span> <span class="hero-title-line hero-title-quiet">Mingħajr il-plastik.</span>',
            "lead": '<p class="hero-lead">Filtru għad-dar b\'abbonament. Id-djar fil-proġett pilota jieħdu l-ewwel xahar u l-installazzjoni b\'xejn.</p>',
            "alt": 'alt="Il-filtru reBottled: ċilindru abjad u rqiq b\'tapp tal-metall u l-logo aħdar ta\' reBottled"',
            "label": '>Indirizz tal-email</label>',
            "placeholder": 'placeholder="L-email tiegħek"',
            "button": '>Avżani</button>',
            "fieldnote": '<p class="signup-note">Aħbarijiet dwar il-proġett pilota biss. Tista\' tneħħi l-abbonament meta trid.</p>',
            "impact_h2": '>Kull tazza hija flixkun li qatt ma jsir.</h2>',
            "impact_lead": '<p class="lead">Aħna intrapriża soċjali. Inkejlu s-suċċess tagħna bil-profitt u bil-fliexken tal-plastik li l-klijenti tagħna ma jibqgħux jixtru, u kull dar tirċievi rapport annwali tal-fliexken.</p>',
            "chart_title": '>Ilma tal-fliexken għal kull persuna fis-sena, fi fliexken ta\' 1.5 L</p>',
            "row_mt": '<div class="bar-row is-local">\n                <dt>Malta</dt>',
            "row_cy": '<div class="bar-row">\n                <dt>Ċipru</dt>',
            "row_es": '<div class="bar-row">\n                <dt>Gżejjer Kanarji</dt>',
            "row_eu": '<dt>Medja tal-UE</dt>',
            "caption": '<figcaption><span class="wall-number">450</span> flixkun fis-sena li dar tipika Maltija ma tibqax tixtri.</figcaption>',
            "grid_aria": "Grilja ta' 450 flixkun żgħir tal-plastik",
            "compare_h2": '>Aħjar għall-gżira, eħfef għalik</h2>',
            "compare_aria": 'aria-label="Ilma tal-fliexken imqabbel ma\' reBottled"',
            "compared_on": '>Paragun</span>',
            "head_bottled": '</svg>Ilma tal-fliexken</span>',
            "data_bottled": 'data-label="Fliexken"',
            "r1h": '>Fliexken tal-plastik fis-sena</span>',
            "r1b": '<span>Madwar 450 kull dar</span>',
            "r1u": '<span><strong>Xejn</strong></span>',
            "r2h": '>Il-ġarr</span>',
            "r2b": '<span>Pakketti mis-supermarket, kull ġimgħa</span>',
            "r2u": '<span><strong>Xejn.</strong> Joħroġ mill-vit tiegħek</span>',
            "r3h": '>It-togħma</span>',
            "r3b": '<span>Tiddependi mill-marka</span>',
            "r3u": '<span><strong>Bla melħ u bla kloru,</strong> bil-minerali miżjuda lura</span>',
            "r4h": '>L-ispiża f\'Malta</span>',
            "r4b": '<span>Madwar €17–30 fix-xahar</span>',
            "r4u": '<span><strong>€24.90</strong> fix-xahar, kollox inkluż</span>',
            "how_h2": '>Faċli tibda, faċli tieqaf</h2>',
            "s1h": '<h3>Nibagħtulek is-sistema</h3>',
            "s1p": '<p>Unità kompatta għal taħt is-sink, bil-vit żgħir tagħha.</p>',
            "s2h": '<h3>Installata f\'30 minuta</h3>',
            "s2p": '<p>Agħmilha int bil-video tagħna. Installazzjoni b\'xejn għad-djar fil-proġett pilota.</p>',
            "s3h": '<h3>Filtri fil-ħin</h3>',
            "s3p": '<p>Jinbidlu b\'dawra waħda, mingħajr għodda. Jekk tieqaf, aħna nieħdu s-sistema lura.</p>',
            "price": '<span class="price-amount">€24.90</span><span class="price-unit">fix-xahar, kollox inkluż</span>',
            "c1": '</svg>Sistema mislufa</li>',
            "c2": '</svg>Il-filtri kollha</li>',
            "c3": '</svg>Appoġġ</li>',
            "c4": '</svg>Rapport annwali tal-fliexken</li>',
            "pricefine": '<p class="fine price-fine">Pjan ta\' 24 xahar. Id-djar fil-proġett pilota jieħdu l-ewwel xahar u l-installazzjoni b\'xejn.</p>',
            "join_h2": '>Kun fost l-ewwel meta nibdew f\'Malta.</h2>',
            "join_lead": '<p class="join-lead">Il-proġett pilota jibda f\'Malta, imbagħad f\'Ċipru u fil-Gżejjer Kanarji. Min jirreġistra kmieni jieħu l-ewwel xahar u l-installazzjoni b\'xejn.</p>',
            "footer": '<p class="footer-line">Ixrob mill-vit, <span class="accent">insa l-plastik.</span></p>',
            "copyright": 'reBottled. Intrapriża soċjali.</p>',
            "langnav": 'aria-label="Lingwa"',
        },
        "js": {
            "sending": "Qed nibagħtu…",
            "notify": "Avżani",
            "errorEmpty": "Jekk jogħġbok daħħal l-email tiegħek.",
            "errorInvalid": "Dan ma jidhirx indirizz tal-email validu. Iċċekkjah, jekk jogħġbok.",
            "errorFailed": "Ġrat xi ħaġa ħażina u ma stajniex nissejvjaw l-email tiegħek. Erġa' pprova.",
            "thanksTitle": "Int fil-lista.",
            "thanksQuestion": "Ħaġa oħra: fejn tgħix? Navżawk meta l-proġett pilota jasal għandek.",
            "thanksPlace": "Nibagħtulek email hekk kif jibda l-proġett pilota {place}, bl-ewwel xahar u l-installazzjoni b'xejn.",
            "thanksOther": "Inżommuk aġġornat, u jekk naslu fiż-żona tiegħek, l-ewwel xahar u l-installazzjoni jkunu b'xejn.",
            "regions": [
                {"id": "malta", "label": "Malta jew Għawdex", "place": "f'Malta"},
                {"id": "cyprus", "label": "Ċipru", "place": "f'Ċipru"},
                {"id": "canary-islands", "label": "Gżejjer Kanarji", "place": "fil-Gżejjer Kanarji"},
                {"id": "other", "label": "Xi mkien ieħor", "place": None},
            ],
        },
    },
}

LANG_LINKS = '''      <nav class="lang-switch" aria-label="Language">
        <a href="./" lang="en" hreflang="en" aria-current="page">English</a>
        <a href="es/" lang="es" hreflang="es">Español</a>
        <a href="cy/" lang="el" hreflang="el">Ελληνικά</a>
        <a href="mt/" lang="mt" hreflang="mt">Malti</a>
      </nav>'''


def lang_links(current):
    items = [("en", "../", "en", "English"), ("es", "../es/", "es", "Español"),
             ("cy", "../cy/", "el", "Ελληνικά"), ("mt", "../mt/", "mt", "Malti")]
    out = []
    for key, href, lang, name in items:
        cur = ' aria-current="page"' if key == current else ""
        if key == current:
            href = "./"
        out.append(f'        <a href="{href}" lang="{lang}" hreflang="{lang}"{cur}>{name}</a>')
    return '      <nav class="lang-switch" aria-label="Language">\n' + "\n".join(out) + "\n      </nav>"


def must_replace(text, old, new, count=1):
    found = text.count(old)
    if found != count:
        raise SystemExit(f"Expected {count}x, found {found}x: {old[:80]!r}")
    return text.replace(old, new)


for code, cfg in LOCALES.items():
    s = src
    s = must_replace(s, LANG_LINKS, lang_links(code))
    t = cfg["t"]

    # bottle grid: aria label and the per-page bottle count
    grid_aria = t.pop("grid_aria")
    g = cfg["grid"]
    style = ""
    if g:
        assert g["cols"] * g["rows"] == g["n"] == g["mcols"] * g["mrows"], code
        style = (f' style="--cols: {g["cols"]}; --rows: {g["rows"]}; --ratio: {g["cols"] / (g["rows"] * 2):.4f};'
                 f' --m-cols: {g["mcols"]}; --m-rows: {g["mrows"]}; --m-ratio: {g["mcols"] / (g["mrows"] * 2):.4f}"')
    s = must_replace(s, COMMON_EN["grid"], f'<div class="bottle-grid" role="img" aria-label="{grid_aria}"{style}></div>')

    for key, en in COMMON_EN.items():
        if key == "grid":
            continue
        if key not in t:
            raise SystemExit(f"{code}: missing translation for {key}")
        s = must_replace(s, en, t[key], REPEATS.get(key, 1))

    s = must_replace(s, '<html lang="en">', f'<html lang="{cfg["lang"]}">')
    # paths: the localised page lives one folder down
    s = must_replace(s, 'href="styles.css"', 'href="../styles.css"')
    s = must_replace(s, 'src="main.js"', 'src="../main.js"')
    s = s.replace('"assets/', '"../assets/').replace(", assets/", ", ../assets/")
    if cfg["fonts"]:
        s = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+">',
                   f'<link rel="stylesheet" href="{cfg["fonts"]}">', s, count=1)
    i18n = json.dumps(cfg["js"], ensure_ascii=False, indent=2)
    i18n = "\n".join("  " + line for line in i18n.splitlines())
    s = must_replace(s, '  <script src="../main.js" defer></script>',
                     '  <script type="application/json" id="i18n">\n' + i18n + '\n  </script>\n  <script src="../main.js" defer></script>')

    os.makedirs(os.path.join(ROOT, code), exist_ok=True)
    with open(os.path.join(ROOT, code, "index.html"), "w", encoding="utf-8") as f:
        f.write(s)
    print("wrote", code)
