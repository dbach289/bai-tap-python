from database import connect_db
from ui import App

conn, cursor = connect_db()

app = App(cursor, conn)
app.mainloop()