"""
Air Quality Platform - MongoDB Python Examples
Demonstrates how to interact with MongoDB from the backend/ingestion services
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from typing import Optional, Dict, List, Any
import os


class MongoDBService:
    """Service class for MongoDB operations (user preferences and dashboard configs)"""
    
    def __init__(self, connection_uri: Optional[str] = None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_uri: MongoDB connection string (defaults to env var MONGO_URI)
        """
        self.uri = connection_uri or os.getenv('MONGO_URI', 'mongodb://localhost:27017/air_quality_config')
        self.db_name = os.getenv('MONGO_DB_NAME', 'air_quality_config')
        
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        
        # Collections
        self.user_preferences = self.db['user_preferences']
        self.dashboard_configs = self.db['dashboard_configs']
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
    
    # ========================================================================
    # USER PREFERENCES
    # ========================================================================
    
    def get_user_preferences(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get preferences for a specific user
        
        Args:
            user_id: User ID from PostgreSQL AppUser table
            
        Returns:
            User preferences document or None if not found
        """
        return self.user_preferences.find_one({'user_id': user_id})
    
    def create_default_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        Create default preferences for a new user
        
        Args:
            user_id: User ID from PostgreSQL AppUser table
            
        Returns:
            Created preferences document
        """
        default_prefs = {
            'user_id': user_id,
            'default_city': 'Bogotá',
            'favorite_pollutants': ['PM2.5', 'PM10'],
            'theme': 'dark',
            'notifications': {
                'email_enabled': True,
                'sms_enabled': False,
                'min_aqi_for_alert': 100,
                'frequency': 'daily'
            },
            'language': 'en',
            'timezone': 'America/Bogota',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        self.user_preferences.insert_one(default_prefs)
        return default_prefs
    
    def update_user_preferences(
        self, 
        user_id: int, 
        preferences: Dict[str, Any]
    ) -> bool:
        """
        Update user preferences (upsert - create if doesn't exist)
        
        Args:
            user_id: User ID
            preferences: Partial or full preferences object
            
        Returns:
            True if successful
        """
        preferences['updated_at'] = datetime.utcnow()
        
        result = self.user_preferences.update_one(
            {'user_id': user_id},
            {
                '$set': preferences,
                '$setOnInsert': {'created_at': datetime.utcnow()}
            },
            upsert=True
        )
        
        return result.acknowledged
    
    def update_notification_settings(
        self,
        user_id: int,
        email_enabled: Optional[bool] = None,
        min_aqi: Optional[int] = None,
        frequency: Optional[str] = None
    ) -> bool:
        """
        Update only notification settings
        
        Args:
            user_id: User ID
            email_enabled: Enable/disable email notifications
            min_aqi: Minimum AQI threshold for alerts
            frequency: Notification frequency
            
        Returns:
            True if successful
        """
        update_fields = {'updated_at': datetime.utcnow()}
        
        if email_enabled is not None:
            update_fields['notifications.email_enabled'] = email_enabled
        if min_aqi is not None:
            update_fields['notifications.min_aqi_for_alert'] = min_aqi
        if frequency is not None:
            update_fields['notifications.frequency'] = frequency
        
        result = self.user_preferences.update_one(
            {'user_id': user_id},
            {'$set': update_fields}
        )
        
        return result.modified_count > 0
    
    def get_users_by_city_and_alert_threshold(
        self,
        city: str,
        min_aqi_threshold: int
    ) -> List[Dict[str, Any]]:
        """
        Find users in a specific city with alerts enabled for a given AQI threshold
        Useful for sending targeted notifications
        
        Args:
            city: City name
            min_aqi_threshold: Minimum AQI value to check
            
        Returns:
            List of matching user preference documents
        """
        return list(self.user_preferences.find({
            'default_city': city,
            'notifications.email_enabled': True,
            'notifications.min_aqi_for_alert': {'$lte': min_aqi_threshold}
        }))
    
    # ========================================================================
    # DASHBOARD CONFIGS
    # ========================================================================
    
    def get_dashboard_config(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get dashboard configuration for a user
        
        Args:
            user_id: User ID from PostgreSQL AppUser table
            
        Returns:
            Dashboard config document or None
        """
        return self.dashboard_configs.find_one({'user_id': user_id})
    
    def create_default_dashboard(self, user_id: int) -> Dict[str, Any]:
        """
        Create default dashboard layout for new user
        
        Args:
            user_id: User ID
            
        Returns:
            Created dashboard config
        """
        default_dashboard = {
            'user_id': user_id,
            'layout_type': 'grid',
            'widgets': [
                {
                    'id': 'widget-current-aqi',
                    'type': 'current_aqi',
                    'title': 'Current Air Quality',
                    'position': {'x': 0, 'y': 0, 'w': 2, 'h': 2},
                    'config': {
                        'pollutant': 'PM2.5',
                        'time_range': '24h'
                    },
                    'enabled': True,
                    'order': 0
                },
                {
                    'id': 'widget-pollutant-chart',
                    'type': 'pollutant_chart',
                    'title': 'PM2.5 Trend',
                    'position': {'x': 2, 'y': 0, 'w': 4, 'h': 2},
                    'config': {
                        'pollutant': 'PM2.5',
                        'time_range': '7d',
                        'chart_type': 'line'
                    },
                    'enabled': True,
                    'order': 1
                },
                {
                    'id': 'widget-health-rec',
                    'type': 'health_recommendation',
                    'title': 'Health Recommendations',
                    'position': {'x': 0, 'y': 2, 'w': 3, 'h': 1},
                    'config': {},
                    'enabled': True,
                    'order': 2
                }
            ],
            'created_at': datetime.utcnow(),
            'last_updated': datetime.utcnow(),
            'version': 1
        }
        
        self.dashboard_configs.insert_one(default_dashboard)
        return default_dashboard
    
    def update_dashboard_layout(
        self,
        user_id: int,
        layout_type: Optional[str] = None,
        widgets: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Update dashboard layout and widgets
        
        Args:
            user_id: User ID
            layout_type: New layout type (grid, freeform, list)
            widgets: Complete widgets array
            
        Returns:
            True if successful
        """
        update_fields = {'last_updated': datetime.utcnow()}
        
        if layout_type:
            update_fields['layout_type'] = layout_type
        if widgets is not None:
            update_fields['widgets'] = widgets
        
        result = self.dashboard_configs.update_one(
            {'user_id': user_id},
            {'$set': update_fields}
        )
        
        return result.modified_count > 0
    
    def toggle_widget(self, user_id: int, widget_id: str, enabled: bool) -> bool:
        """
        Enable or disable a specific widget
        
        Args:
            user_id: User ID
            widget_id: Widget unique identifier
            enabled: True to enable, False to disable
            
        Returns:
            True if successful
        """
        result = self.dashboard_configs.update_one(
            {
                'user_id': user_id,
                'widgets.id': widget_id
            },
            {
                '$set': {
                    'widgets.$.enabled': enabled,
                    'last_updated': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    def add_widget(
        self,
        user_id: int,
        widget: Dict[str, Any]
    ) -> bool:
        """
        Add a new widget to user's dashboard
        
        Args:
            user_id: User ID
            widget: Widget configuration object
            
        Returns:
            True if successful
        """
        result = self.dashboard_configs.update_one(
            {'user_id': user_id},
            {
                '$push': {'widgets': widget},
                '$set': {'last_updated': datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0
    
    def remove_widget(self, user_id: int, widget_id: str) -> bool:
        """
        Remove a widget from dashboard
        
        Args:
            user_id: User ID
            widget_id: Widget ID to remove
            
        Returns:
            True if successful
        """
        result = self.dashboard_configs.update_one(
            {'user_id': user_id},
            {
                '$pull': {'widgets': {'id': widget_id}},
                '$set': {'last_updated': datetime.utcnow()}
            }
        )
        
        return result.modified_count > 0


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Demonstrates how to use the MongoDB service"""
    
    # Initialize service
    mongo_service = MongoDBService()
    
    try:
        # Create preferences for new user
        user_id = 123
        prefs = mongo_service.create_default_preferences(user_id)
        print(f"Created preferences for user {user_id}: {prefs}")
        
        # Update specific preference
        mongo_service.update_user_preferences(
            user_id,
            {'theme': 'light', 'default_city': 'Medellín'}
        )
        
        # Get preferences
        user_prefs = mongo_service.get_user_preferences(user_id)
        print(f"User preferences: {user_prefs}")
        
        # Update notification settings
        mongo_service.update_notification_settings(
            user_id,
            email_enabled=True,
            min_aqi=150
        )
        
        # Create default dashboard
        dashboard = mongo_service.create_default_dashboard(user_id)
        print(f"Created dashboard for user {user_id}")
        
        # Toggle widget
        mongo_service.toggle_widget(user_id, 'widget-current-aqi', False)
        
        # Add new widget
        new_widget = {
            'id': 'widget-station-map',
            'type': 'station_map',
            'title': 'Nearby Stations',
            'position': {'x': 3, 'y': 2, 'w': 3, 'h': 2},
            'config': {},
            'enabled': True,
            'order': 3
        }
        mongo_service.add_widget(user_id, new_widget)
        
        # Find users for targeted notifications
        users_to_notify = mongo_service.get_users_by_city_and_alert_threshold(
            'Bogotá',
            min_aqi_threshold=120
        )
        print(f"Found {len(users_to_notify)} users to notify in Bogotá")
        
    finally:
        mongo_service.close()


if __name__ == '__main__':
    example_usage()
