# 🔌 Guide des Intégrations HBNB

## 📋 Table des Matières
1. [Webhooks](#webhooks)
2. [API Externes](#api-externes)
3. [Services de Paiement](#services-de-paiement)
4. [Authentification OAuth](#authentification-oauth)
5. [Notifications](#notifications)

## 🪝 Webhooks

### Configuration des Webhooks
```python
from flask import request, jsonify
import hmac
import hashlib

def verify_webhook_signature(request_data, signature, secret):
    """Vérifie la signature du webhook."""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        request_data,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.route('/webhooks/booking', methods=['POST'])
def booking_webhook():
    signature = request.headers.get('X-Webhook-Signature')
    if not verify_webhook_signature(request.data, signature, WEBHOOK_SECRET):
        return jsonify({'error': 'Invalid signature'}), 401
    
    # Traitement du webhook
    data = request.json
    event_type = data['event']
    
    if event_type == 'booking.confirmed':
        process_booking_confirmation(data['booking_id'])
    elif event_type == 'booking.cancelled':
        process_booking_cancellation(data['booking_id'])
        
    return jsonify({'status': 'processed'}), 200
```

### Événements Disponibles
```markdown
📢 Types d'Événements
├── Réservations
│   ├── booking.created
│   ├── booking.confirmed
│   ├── booking.cancelled
│   └── booking.completed
├── Paiements
│   ├── payment.succeeded
│   ├── payment.failed
│   └── payment.refunded
└── Utilisateurs
    ├── user.registered
    └── user.updated
```

## 🌐 API Externes

### Intégration Maps
```python
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class LocationService:
    def __init__(self):
        self.geocoder = Nominatim(user_agent="hbnb")

    def geocode_address(self, address: str) -> dict:
        """Convertit une adresse en coordonnées."""
        location = self.geocoder.geocode(address)
        if location:
            return {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address
            }
        raise ValueError("Address not found")

    def calculate_distance(self, point1: tuple, point2: tuple) -> float:
        """Calcule la distance entre deux points."""
        return geodesic(point1, point2).kilometers
```

### Service Email (SendGrid)
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(api_key=SENDGRID_API_KEY)

    def send_booking_confirmation(self, booking):
        message = Mail(
            from_email='bookings@hbnb.com',
            to_emails=booking.guest.email,
            subject='Confirmation de réservation',
            html_content=render_template(
                'emails/booking_confirmation.html',
                booking=booking
            )
        )
        
        try:
            response = self.client.send(message)
            return response.status_code
        except Exception as e:
            logger.error(f"Email error: {str(e)}")
            raise
```

## 💳 Services de Paiement

### Intégration Stripe
```python
import stripe
stripe.api_key = STRIPE_SECRET_KEY

class PaymentService:
    @staticmethod
    def create_payment_intent(booking):
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(booking.total_price * 100),  # Conversion en centimes
                currency='eur',
                customer=booking.guest.stripe_customer_id,
                metadata={
                    'booking_id': booking.id,
                    'guest_id': booking.guest_id
                }
            )
            return intent.client_secret
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {str(e)}")
            raise PaymentError(str(e))

    @staticmethod
    def process_refund(booking):
        try:
            refund = stripe.Refund.create(
                payment_intent=booking.payment_intent_id
            )
            return refund.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Refund error: {str(e)}")
            raise RefundError(str(e))
```

## 🔑 Authentification OAuth

### Configuration Providers
```python
from flask_oauthlib.client import OAuth

oauth = OAuth(app)

# Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key=GOOGLE_CLIENT_ID,
    consumer_secret=GOOGLE_CLIENT_SECRET,
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)

@app.route('/login/google')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={}'.format(
            request.args['error_reason']
        )
    
    # Traitement de l'authentification réussie
    user_info = google.get('userinfo')
    return process_oauth_login(user_info.data)
```

## 📱 Notifications

### Service de Push Notifications
```python
from firebase_admin import messaging

class NotificationService:
    def send_push_notification(self, user_id: str, title: str, body: str):
        # Récupérer les tokens FCM de l'utilisateur
        user = User.query.get(user_id)
        if not user or not user.fcm_tokens:
            return
            
        message = messaging.MulticastMessage(
            tokens=user.fcm_tokens,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data={
                'click_action': 'FLUTTER_NOTIFICATION_CLICK',
                'type': 'booking_update'
            }
        )
        
        try:
            response = messaging.send_multicast(message)
            logger.info(f"Successfully sent message: {response}")
        except Exception as e:
            logger.error(f"Error sending notification: {str(e)}")
```

### Configuration Websocket (temps réel)
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False
    
    join_room(f"user_{current_user.id}")
    emit('status', {'status': 'connected'})

@socketio.on('message')
def handle_message(data):
    recipient_id = data.get('recipient_id')
    message = data.get('message')
    
    # Sauvegarder le message
    chat_message = ChatMessage(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=message
    )
    db.session.add(chat_message)
    db.session.commit()
    
    # Émettre vers le destinataire
    emit('new_message', {
        'sender_id': current_user.id,
        'message': message,
        'timestamp': chat_message.created_at.isoformat()
    }, room=f"user_{recipient_id}")
```

D'accord, je continue le guide d'intégrations avec les sections suivantes :

## 📊 Analytiques et Rapports

### Service d'Analytics
```python
class AnalyticsService:
    def track_event(self, event_name: str, user_id: str, properties: dict):
        """Enregistre un événement analytique."""
        analytics_event = AnalyticsEvent(
            name=event_name,
            user_id=user_id,
            properties=properties,
            timestamp=datetime.utcnow()
        )
        db.session.add(analytics_event)
        db.session.commit()

    def get_booking_metrics(self, start_date: date, end_date: date) -> dict:
        """Calcule les métriques de réservation."""
        return {
            'total_bookings': Booking.query.filter(
                Booking.created_at.between(start_date, end_date)
            ).count(),
            'total_revenue': db.session.query(
                func.sum(Booking.total_price)
            ).filter(
                Booking.created_at.between(start_date, end_date)
            ).scalar() or 0,
            'average_price': db.session.query(
                func.avg(Booking.total_price)
            ).filter(
                Booking.created_at.between(start_date, end_date)
            ).scalar() or 0
        }
```

## 🗺️ Service de Cartographie

### Intégration Mapbox
```python
class MapService:
    def __init__(self):
        self.client = MapboxClient(access_token=MAPBOX_TOKEN)

    def get_place_suggestions(self, query: str) -> list:
        """Obtient des suggestions d'adresses."""
        response = self.client.places.forward(query)
        return [{
            'place_name': feature['place_name'],
            'coordinates': feature['geometry']['coordinates']
        } for feature in response.json()['features']]

    def calculate_route(self, origin: tuple, destination: tuple) -> dict:
        """Calcule l'itinéraire entre deux points."""
        response = self.client.directions(
            [origin, destination],
            'mapbox/driving'
        )
        route = response.json()['routes'][0]
        return {
            'distance': route['distance'],
            'duration': route['duration'],
            'polyline': route['geometry']
        }
```

## 📱 Service de Médias

### Gestion des Images
```python
from PIL import Image
import boto3

class MediaService:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def process_image(self, image_file, sizes: dict) -> dict:
        """Traite et redimensionne une image."""
        urls = {}
        for size_name, dimensions in sizes.items():
            img = Image.open(image_file)
            img.thumbnail(dimensions)
            buffer = BytesIO()
            img.save(buffer, format='JPEG')
            
            # Upload vers S3
            key = f"images/{uuid.uuid4()}-{size_name}.jpg"
            self.s3.put_object(
                Bucket=S3_BUCKET,
                Key=key,
                Body=buffer.getvalue(),
                ContentType='image/jpeg'
            )
            urls[size_name] = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
        return urls
```

## 📧 Service de Communication

### Gestion des Templates
```python
class CommunicationService:
    def __init__(self):
        self.email_client = SendGridAPIClient(SENDGRID_API_KEY)
        self.sms_client = TwilioClient(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_template_email(self, template_id: str, user: User, data: dict):
        """Envoie un email basé sur un template."""
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=user.email
        )
        message.template_id = template_id
        message.dynamic_template_data = data
        
        try:
            response = self.email_client.send(message)
            return response.status_code == 202
        except Exception as e:
            logger.error(f"Email error: {str(e)}")
            return False

    def send_sms_notification(self, phone: str, message: str):
        """Envoie une notification SMS."""
        try:
            message = self.sms_client.messages.create(
                body=message,
                from_=TWILIO_PHONE,
                to=phone
            )
            return message.sid
        except Exception as e:
            logger.error(f"SMS error: {str(e)}")
            return None
```

## 🔄 Service de Synchronisation

### Synchronisation des Calendriers
```python
from icalendar import Calendar, Event

class CalendarService:
    def generate_ical(self, place: Place) -> str:
        """Génère un fichier iCal pour un logement."""
        cal = Calendar()
        cal.add('prodid', '-//HBNB//Calendar')
        cal.add('version', '2.0')
        
        for booking in place.bookings:
            event = Event()
            event.add('summary', f'Réservation: {place.title}')
            event.add('dtstart', booking.check_in)
            event.add('dtend', booking.check_out)
            event.add('description', f'Réservation par {booking.guest.name}')
            cal.add_component(event)
            
        return cal.to_ical().decode('utf-8')

    def import_external_calendar(self, url: str) -> list:
        """Importe un calendrier externe."""
        response = requests.get(url)
        cal = Calendar.from_ical(response.text)
        
        bookings = []
        for event in cal.walk('VEVENT'):
            bookings.append({
                'start': event.get('dtstart').dt,
                'end': event.get('dtend').dt,
                'description': event.get('description', '')
            })
        return bookings
```
Tu as raison, je vais continuer avec TOUS les services restants dans ce même fichier.

## 💬 Service de Chat

```python
class ChatService:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        
    def send_message(self, sender_id: str, recipient_id: str, content: str) -> Message:
        """Envoie un message."""
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
        
        # Notifications temps réel
        self.notify_new_message(recipient_id, message)
        return message
        
    def get_conversation(self, user1_id: str, user2_id: str, page: int = 1) -> list:
        """Récupère une conversation."""
        return Message.query.filter(
            or_(
                and_(Message.sender_id == user1_id, Message.recipient_id == user2_id),
                and_(Message.sender_id == user2_id, Message.recipient_id == user1_id)
            )
        ).order_by(Message.created_at.desc()).paginate(page=page, per_page=50)

    def translate_message(self, message: str, target_language: str) -> str:
        """Traduit un message."""
        translator = Translator()
        return translator.translate(message, dest=target_language).text
```

## 🔍 Service de Recherche

```python
class SearchService:
    def __init__(self):
        self.es = Elasticsearch([ES_HOST])
        
    def index_place(self, place: Place):
        """Indexe un logement dans Elasticsearch."""
        doc = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'location': {
                'lat': place.latitude,
                'lon': place.longitude
            },
            'amenities': [a.name for a in place.amenities],
            'created_at': place.created_at.isoformat()
        }
        self.es.index(index='places', id=place.id, body=doc)
        
    def search_places(self, query: dict) -> list:
        """Recherche des logements."""
        must = []
        if query.get('text'):
            must.append({
                'multi_match': {
                    'query': query['text'],
                    'fields': ['title^3', 'description']
                }
            })
            
        if query.get('price_range'):
            must.append({
                'range': {
                    'price': {
                        'gte': query['price_range'][0],
                        'lte': query['price_range'][1]
                    }
                }
            })
            
        if query.get('location'):
            must.append({
                'geo_distance': {
                    'distance': f"{query['radius']}km",
                    'location': {
                        'lat': query['location'][0],
                        'lon': query['location'][1]
                    }
                }
            })
            
        body = {
            'query': {'bool': {'must': must}},
            'sort': [{'_score': 'desc'}, {'created_at': 'desc'}]
        }
        
        results = self.es.search(index='places', body=body)
        return [hit['_source'] for hit in results['hits']['hits']]
```

## 🎯 Service de Recommandations

```python
class RecommendationService:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        
    def track_view(self, user_id: str, place_id: str):
        """Enregistre une vue de logement."""
        key = f"user:views:{user_id}"
        self.redis.zadd(key, {place_id: time.time()})
        
    def get_similar_places(self, place_id: str) -> list:
        """Trouve des logements similaires."""
        place = Place.query.get(place_id)
        if not place:
            return []
            
        return Place.query.filter(
            Place.id != place_id,
            Place.price.between(place.price * 0.8, place.price * 1.2),
            func.ST_Distance_Sphere(
                func.ST_MakePoint(Place.longitude, Place.latitude),
                func.ST_MakePoint(place.longitude, place.latitude)
            ) < 5000  # 5km
        ).order_by(func.random()).limit(10).all()
        
    def get_personalized_recommendations(self, user_id: str) -> list:
        """Obtient des recommandations personnalisées."""
        # Historique des vues
        viewed = self.redis.zrange(f"user:views:{user_id}", 0, -1)
        
        # Préférences utilisateur
        user = User.query.get(user_id)
        preferences = UserPreference.query.filter_by(user_id=user_id).first()
        
        query = Place.query.filter(Place.id.notin_(viewed))
        
        if preferences:
            if preferences.max_price:
                query = query.filter(Place.price <= preferences.max_price)
            if preferences.preferred_location:
                query = query.filter(
                    func.ST_Distance_Sphere(
                        func.ST_MakePoint(Place.longitude, Place.latitude),
                        func.ST_MakePoint(
                            preferences.preferred_location[1],
                            preferences.preferred_location[0]
                        )
                    ) < preferences.preferred_radius * 1000
                )
        
        return query.order_by(func.random()).limit(20).all()
```

## 📅 Service de Calendrier

```python
class CalendarSyncService:
    def __init__(self):
        self.redis = Redis(host=REDIS_HOST, port=REDIS_PORT)
        
    def sync_external_calendar(self, place_id: str, calendar_url: str):
        """Synchronise un calendrier externe."""
        try:
            response = requests.get(calendar_url)
            cal = Calendar.from_ical(response.text)
            
            for event in cal.walk('VEVENT'):
                start = event.get('dtstart').dt
                end = event.get('dtend').dt
                
                # Créer une période bloquée
                blocked_period = BlockedPeriod(
                    place_id=place_id,
                    start_date=start,
                    end_date=end,
                    reason='external_calendar'
                )
                db.session.add(blocked_period)
            
            db.session.commit()
            self.redis.set(f"calendar:last_sync:{place_id}", datetime.now().isoformat())
            
        except Exception as e:
            logger.error(f"Calendar sync error: {str(e)}")
            raise CalendarSyncError(str(e))
            
    def check_availability(self, place_id: str, start_date: date, end_date: date) -> bool:
        """Vérifie la disponibilité d'un logement."""
        # Vérifier les réservations
        existing_booking = Booking.query.filter(
            Booking.place_id == place_id,
            Booking.status.in_(['confirmed', 'pending']),
            or_(
                and_(
                    Booking.check_in <= start_date,
                    Booking.check_out > start_date
                ),
                and_(
                    Booking.check_in < end_date,
                    Booking.check_out >= end_date
                ),
                and_(
                    Booking.check_in >= start_date,
                    Booking.check_out <= end_date
                )
            )
        ).first()
        
        if existing_booking:
            return False
            
        # Vérifier les périodes bloquées
        blocked_period = BlockedPeriod.query.filter(
            BlockedPeriod.place_id == place_id,
            or_(
                and_(
                    BlockedPeriod.start_date <= start_date,
                    BlockedPeriod.end_date > start_date
                ),
                and_(
                    BlockedPeriod.start_date < end_date,
                    BlockedPeriod.end_date >= end_date
                ),
                and_(
                    BlockedPeriod.start_date >= start_date,
                    BlockedPeriod.end_date <= end_date
                )
            )
        ).first()
        
        return not bool(blocked_period)
```

## 🔔 Service de Notifications

```python
class NotificationService:
    def __init__(self):
        self.fcm = messaging.FCMApp()
        self.email_service = EmailService()
        self.sms_service = SMSService()
        
    def send_multi_channel_notification(self, user_id: str, notification: dict):
        """Envoie une notification sur plusieurs canaux."""
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")
            
        results = {
            'push': False,
            'email': False,
            'sms': False
        }
        
        # Notification push
        if user.fcm_tokens:
            try:
                message = messaging.MulticastMessage(
                    tokens=user.fcm_tokens,
                    notification=messaging.Notification(
                        title=notification['title'],
                        body=notification['body']
                    ),
                    data=notification.get('data', {})
                )
                response = messaging.send_multicast(message)
                results['push'] = response.success_count > 0
            except Exception as e:
                logger.error(f"Push notification error: {str(e)}")
                
        # Email
        if user.email_notifications_enabled:
            try:
                results['email'] = self.email_service.send_notification(
                    user.email,
                    notification['title'],
                    notification['body']
                )
            except Exception as e:
                logger.error(f"Email notification error: {str(e)}")
                
        # SMS
        if user.sms_notifications_enabled and user.phone:
            try:
                results['sms'] = self.sms_service.send_notification(
                    user.phone,
                    notification['body']
                )
            except Exception as e:
                logger.error(f"SMS notification error: {str(e)}")
                
        return results
```

Voilà un fichier d'intégrations complet avec tous les services principaux. Voulez-vous que je passe au prochain guide complet ?
