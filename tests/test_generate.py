import pytest
from enum import Enum

from SMTG import generate


def test_context_1():
    context = {}

    pass




class TestTemplate1():
    template = ("Hallo {{name}},\nVielen Dank für deine Anmeldung zur Jährlichen Mitgliederversammlung des deutschen "
                "Pudelzüchtervereins.\nWir freuen uns, dass du als {{attending}} teilnehmen wirst.\n"
                "Als {{attending}} hast du folgende Aufgaben:\n"
                "{? attending == 'speaker' and len(vortraege)>0 | Du musst {{len(vortraege)}} {? len("
                "vortraege)==1 | Vortrag | Vorträge ?} halten.\n Du hälst: {{vortraege}}?}"
                "Liebe Grüße,\nDer Vorstand")

    def test_1(self):
        context = {"name": "Hans", "attending": "speaker", "vortraege": ["Vortrag 1", "Vortrag 2"],
                   "rabatt": 30}
        text = generate(self.template, **context)
        print("s")

    pass
