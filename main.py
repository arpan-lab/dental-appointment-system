
from langchain_core.messages import HumanMessage

from app.graph.workflow import build_workflow


def main():

    graph = build_workflow()

    thread_id = "dental-chat-001"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print("\nDental Appointment Assistant")
    print("Type 'exit' to end the conversation.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("\nAssistant: Goodbye!")
            break

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ],
                "patient_id": "P001",
                "intent": None,
                "doctor_id": None,
                "appointment_id": None,
                "date": None,
                "time": None,
                "response": None,
            },
            config=config,
        )

        if result.get("intent") == "FINISH":
            print("\nAssistant: You're welcome! Have a great day!")
            break

        print("\nAssistant:", result.get("response"))


if __name__ == "__main__":
    main()

