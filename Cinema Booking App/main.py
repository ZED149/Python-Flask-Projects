

# this is the main() for Cinema Booking Application


from webapp import homepage
from webapp import bookingpage
from webapp import detailspage
from webapp import successpage
from flask_session import Session

app = homepage.app
app.add_url_rule('/', view_func=homepage.HomePage.as_view('home_page'))
app.add_url_rule('/booking', view_func=bookingpage.BookingPage.as_view('booking_page'))
app.add_url_rule('/details', view_func=detailspage.DetailsPage.as_view('details_page'))
app.add_url_rule('/success', view_func=successpage.SuccessPage.as_view('success_page'))
app.run()

