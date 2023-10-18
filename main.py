from kivy.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import pdfplumber
from transformers import pipeline  # Make sure you have the 'transformers' library installed.

# Define the question_answering pipeline
question_answering = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

class MyTabbedApp(App):
    def build(self):
        return MainLayout()

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.tabbed_panel = MyTabbedPanel()
        self.add_widget(self.tabbed_panel)

class MyTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super(MyTabbedPanel, self).__init__(**kwargs)

        self.online_tab = OnlineTab(text='Online')
        self.offline_tab = OfflineTab(text='Offline')

        self.add_widget(self.online_tab)
        self.add_widget(self.offline_tab)

class OnlineTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super(OnlineTab, self).__init__(**kwargs)
        self.content = OnlineContent()

class OnlineContent(BoxLayout):
    def __init__(self, **kwargs):
        super(OnlineContent, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.chat_label = Label(text="Chat:")
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self.question_input = TextInput(hint_text="Ask a question", multiline=False)
        self.send_button = Button(text="Send", size_hint=(None, None), size=(100, 50))
        self.send_button.bind(on_release=self.send_question)

        self.add_widget(self.chat_label)
        self.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.chat_layout)
        self.add_widget(self.question_input)
        self.add_widget(self.send_button)

    def send_question(self, instance):
        question = self.question_input.text
        response = "Online: " + question
        chat_item = Label(text=f"You: {question}\nOnline: {response}")
        self.chat_layout.add_widget(chat_item)
        self.question_input.text = ""

class OfflineTab(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super(OfflineTab, self).__init__(**kwargs)
        self.content = OfflineContent()

class OfflineContent(BoxLayout):
    def __init__(self, **kwargs):
        super(OfflineContent, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.chat_label = Label(text="Question:")
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))

        self.question_input = TextInput(hint_text="Ask a question", multiline=False)
        self.send_button = Button(text="Send", size_hint=(None, None), size=(100, 50))
        self.send_button.bind(on_release=self.send_question)

        self.answer_label = Label(text="Answer:")

        self.add_widget(self.chat_label)
        self.add_widget(self.scroll_view)
        self.scroll_view.add_widget(self.chat_layout)
        self.add_widget(self.question_input)
        self.add_widget(self.send_button)
        self.add_widget(self.answer_label)

    def send_question(self, instance):
        question = self.question_input.text
        response = "Offline: " + question
        chat_item = Label(text=f"You: {question}")
        self.chat_layout.add_widget(chat_item)
        self.question_input.text = ""

        # Call a function to extract PDF text and get the answer
        pdf_path = "input1.pdf"
        pdf_text = extract_text_from_pdf(pdf_path)
        result = question_answering(question=question, context=pdf_text)
        answer = result["answer"]
        answer_label = Label(text=f"Answer: {answer}")
        self.add_widget(answer_label)

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == '__main__':
    MyTabbedApp().run()
