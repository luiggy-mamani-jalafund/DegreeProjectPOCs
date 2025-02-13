from typing import Text, List, Any, Dict

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset

APPOINTMENTS_AVAILABLE = {
    "lunes": ["9:00", "10:00", "11:00", "15:00", "16:00"],
    "martes": ["9:00", "10:00", "14:00", "15:00"],
    "miercoles": ["11:00", "14:00", "15:00", "16:00"],
    "jueves": ["9:00", "10:00", "11:00", "14:00"],
    "viernes": ["10:00", "11:00", "15:00", "16:00"],
}


class ValidateRestaurantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"

    @staticmethod
    def appointments_db() -> dict[str, list[str]]:
        return APPOINTMENTS_AVAILABLE

    def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        time_to_check = slot_value
        available_days = [
            day
            for day, appointments in self.appointments_db().items()
            if time_to_check in appointments
        ]

        if len(available_days) == 0:
            dispatcher.utter_message(
                "lo siento, no tenemos ese horario disponible, tenemos los siguientes horarios disponibles:"
            )
            for day, hours in self.appointments_db().items():
                dispatcher.utter_message(
                    f"el {day} tiene las siguientes horas disponibles: {', '.join(hours)}"
                )

            return {"time": None}

        time = tracker.get_slot("time")
        day = tracker.get_slot("day")
        if day:
            return {"time": slot_value}
        elif time and day:
            return {"time": slot_value}
        else:
            dispatcher.utter_message(
                f"ok, los dias que tienen ese horario disponible son los dias {', '.join(available_days)}"
            )
            return {"time": slot_value}

    def validate_day(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        day_to_check = slot_value.lower()
        avaliable_hours = self.appointments_db().get(day_to_check)
        if avaliable_hours is None:
            dispatcher.utter_message(
                f"lo siento, no tenemos ese dia disponible, los dias disponibles son {', '.join(self.appointments_db().values())}"
            )
            return {"day": None}

        time = tracker.get_slot("time")
        day = tracker.get_slot("day")
        if time:
            return {"day": slot_value}
        elif time and day:
            return {"day": slot_value}
        else:
            dispatcher.utter_message(
                f"perfecto, los horarios disponibles para el {slot_value} son {', '.join(avaliable_hours)}"
            )
            return {"day": slot_value}


class ActionSubmmitForm(Action):

    def name(self) -> Text:
        return "action_submmit_form"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        day = tracker.get_slot("day")
        dispatcher.utter_message(f"He agendado tu cita para el {day} a las {time}")
        dispatcher.utter_message("Te esperamos!")
        dispatcher.utter_message("hay algo mas en que pueda ayudarte?")

        return [AllSlotsReset()]
