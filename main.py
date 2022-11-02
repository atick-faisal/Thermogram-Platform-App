from ui import App
from utils import SerialPort, UiState

app = App()
port = SerialPort(115200).open()
ui_state = UiState(port, app.update_thermogram)

app.add_record_callback(ui_state.record_data)
ui_state.start()
app.mainloop()
