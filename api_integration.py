import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class APIIntegration:
    def __init__(self, base_url: str, api_key: str):
        """
        Inicializa la integración con la API.
        
        Args:
            base_url (str): URL base de la API
            api_key (str): Clave de API para autenticación
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Realiza una petición a la API.
        
        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE)
            endpoint (str): Endpoint de la API
            data (Optional[Dict]): Datos a enviar en la petición
            
        Returns:
            Dict: Respuesta de la API
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error en la petición a {url}: {str(e)}")
            return {'success': False, 'message': str(e)}

class TicketAPI(APIIntegration):
    def create_ticket(self, title: str, content: str, department_id: int, 
                     author_id: int, priority: str = 'normal') -> Dict:
        """
        Crea un nuevo ticket.
        
        Args:
            title (str): Título del ticket
            content (str): Contenido del ticket
            department_id (int): ID del departamento
            author_id (int): ID del autor
            priority (str): Prioridad del ticket (low, normal, high)
            
        Returns:
            Dict: Respuesta de la API
        """
        data = {
            'title': title,
            'content': content,
            'department_id': department_id,
            'author_id': author_id,
            'priority': priority,
            'created_at': datetime.now().isoformat()
        }
        return self._make_request('POST', '/ticket/create', data)

    def get_ticket(self, ticket_id: int) -> Dict:
        """
        Obtiene un ticket por su ID.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        return self._make_request('GET', f'/ticket/{ticket_id}')

    def add_comment(self, ticket_id: int, content: str, author_id: int) -> Dict:
        """
        Añade un comentario a un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            content (str): Contenido del comentario
            author_id (int): ID del autor
            
        Returns:
            Dict: Respuesta de la API
        """
        data = {
            'ticket_id': ticket_id,
            'content': content,
            'author_id': author_id,
            'created_at': datetime.now().isoformat()
        }
        return self._make_request('POST', '/ticket/comment', data)

    def close_ticket(self, ticket_id: int) -> Dict:
        """
        Cierra un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        return self._make_request('POST', f'/ticket/{ticket_id}/close')

    def reopen_ticket(self, ticket_id: int) -> Dict:
        """
        Reabre un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        return self._make_request('POST', f'/ticket/{ticket_id}/reopen')

    def search_tickets(self, query: str, department_id: Optional[int] = None, 
                      status: Optional[str] = None) -> Dict:
        """
        Busca tickets según criterios.
        
        Args:
            query (str): Término de búsqueda
            department_id (Optional[int]): ID del departamento
            status (Optional[str]): Estado del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        params = {'query': query}
        if department_id:
            params['department_id'] = department_id
        if status:
            params['status'] = status
            
        return self._make_request('GET', '/ticket/search', params)

    def get_ticket_authors(self, ticket_id: int) -> Dict:
        """
        Obtiene los autores de un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        return self._make_request('GET', f'/ticket/{ticket_id}/authors')

    def add_tag(self, ticket_id: int, tag_name: str) -> Dict:
        """
        Añade una etiqueta a un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            tag_name (str): Nombre de la etiqueta
            
        Returns:
            Dict: Respuesta de la API
        """
        data = {
            'ticket_id': ticket_id,
            'tag_name': tag_name
        }
        return self._make_request('POST', '/ticket/tag', data)

    def remove_tag(self, ticket_id: int, tag_name: str) -> Dict:
        """
        Elimina una etiqueta de un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            tag_name (str): Nombre de la etiqueta
            
        Returns:
            Dict: Respuesta de la API
        """
        data = {
            'ticket_id': ticket_id,
            'tag_name': tag_name
        }
        return self._make_request('DELETE', '/ticket/tag', data)

    def get_ticket_tags(self, ticket_id: int) -> Dict:
        """
        Obtiene las etiquetas de un ticket.
        
        Args:
            ticket_id (int): ID del ticket
            
        Returns:
            Dict: Respuesta de la API
        """
        return self._make_request('GET', f'/ticket/{ticket_id}/tags') 