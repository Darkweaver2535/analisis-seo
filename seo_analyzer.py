import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
import time

class SEOAnalyzer:
    def __init__(self):
        self.seo_guidelines = {
            'title': {
                'name': 'Título de la página',
                'description': 'El título debe tener entre 30-60 caracteres y ser descriptivo',
                'weight': 15,
                'guide': 'El título es crucial para SEO. Debe incluir palabras clave principales y ser atractivo para usuarios.'
            },
            'meta_description': {
                'name': 'Meta descripción',
                'description': 'Debe tener entre 150-160 caracteres y ser relevante',
                'weight': 10,
                'guide': 'La meta descripción aparece en resultados de búsqueda y debe incentivar el clic.'
            },
            'h1_tag': {
                'name': 'Etiqueta H1',
                'description': 'Debe existir solo una etiqueta H1 por página',
                'weight': 12,
                'guide': 'El H1 debe contener la palabra clave principal y describir el contenido de la página.'
            },
            'heading_structure': {
                'name': 'Estructura de encabezados',
                'description': 'Uso correcto de H1, H2, H3, etc. en orden jerárquico',
                'weight': 8,
                'guide': 'Los encabezados organizan el contenido y ayudan a los motores de búsqueda a entender la estructura.'
            },
            'images_alt': {
                'name': 'Texto alternativo en imágenes',
                'description': 'Todas las imágenes deben tener atributo alt descriptivo',
                'weight': 8,
                'guide': 'El texto alt mejora la accesibilidad y ayuda a los motores de búsqueda a entender las imágenes.'
            },
            'internal_links': {
                'name': 'Enlaces internos',
                'description': 'La página debe tener enlaces hacia otras páginas del sitio',
                'weight': 10,
                'guide': 'Los enlaces internos distribuyen la autoridad de página y mejoran la navegación.'
            },
            'external_links': {
                'name': 'Enlaces externos',
                'description': 'Enlaces hacia sitios externos de calidad',
                'weight': 5,
                'guide': 'Enlaces a fuentes confiables pueden mejorar la credibilidad del contenido.'
            },
            'https_ssl': {
                'name': 'Certificado SSL (HTTPS)',
                'description': 'El sitio debe usar protocolo HTTPS',
                'weight': 10,
                'guide': 'HTTPS es un factor de ranking y mejora la seguridad y confianza del usuario.'
            },
            'mobile_viewport': {
                'name': 'Optimización móvil',
                'description': 'Meta tag viewport configurado correctamente',
                'weight': 12,
                'guide': 'La optimización móvil es esencial ya que Google usa indexación mobile-first.'
            },
            'page_speed': {
                'name': 'Velocidad de carga',
                'description': 'Tiempo de respuesta del servidor',
                'weight': 10,
                'guide': 'La velocidad de carga afecta la experiencia del usuario y el ranking en buscadores.'
            }
        }

    def analyze_seo(self, url):
        try:
            # Medir tiempo de carga
            start_time = time.time()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            load_time = time.time() - start_time
            
            # Usar html.parser en lugar de lxml
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = {
                'url': url,
                'checks': {},
                'overall_score': 0,
                'total_points': 0,
                'earned_points': 0
            }
            
            # Análisis individual de cada aspecto
            results['checks']['title'] = self._check_title(soup)
            results['checks']['meta_description'] = self._check_meta_description(soup)
            results['checks']['h1_tag'] = self._check_h1_tag(soup)
            results['checks']['heading_structure'] = self._check_heading_structure(soup)
            results['checks']['images_alt'] = self._check_images_alt(soup)
            results['checks']['internal_links'] = self._check_internal_links(soup, url)
            results['checks']['external_links'] = self._check_external_links(soup, url)
            results['checks']['https_ssl'] = self._check_https(url)
            results['checks']['mobile_viewport'] = self._check_mobile_viewport(soup)
            results['checks']['page_speed'] = self._check_page_speed(load_time)
            
            # Calcular puntuación general
            for check_name, check_result in results['checks'].items():
                weight = self.seo_guidelines[check_name]['weight']
                results['total_points'] += weight
                if check_result['passed']:
                    results['earned_points'] += weight
            
            results['overall_score'] = round((results['earned_points'] / results['total_points']) * 100, 1)
            
            return results
            
        except Exception as e:
            return {'error': f'Error al analizar la URL: {str(e)}'}

    def _check_title(self, soup):
        title_tag = soup.find('title')
        if not title_tag:
            return {
                'passed': False,
                'score': 0,
                'message': 'No se encontró etiqueta title',
                'details': 'La página no tiene título'
            }
        
        title_text = title_tag.get_text().strip()
        length = len(title_text)
        
        if 30 <= length <= 60:
            return {
                'passed': True,
                'score': 100,
                'message': f'Título óptimo ({length} caracteres)',
                'details': f'"{title_text}"'
            }
        elif length > 0:
            return {
                'passed': False,
                'score': 50,
                'message': f'Título subóptimo ({length} caracteres)',
                'details': f'"{title_text}" - Recomendado: 30-60 caracteres'
            }
        else:
            return {
                'passed': False,
                'score': 0,
                'message': 'Título vacío',
                'details': 'El título no tiene contenido'
            }

    def _check_meta_description(self, soup):
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content'):
            return {
                'passed': False,
                'score': 0,
                'message': 'No se encontró meta descripción',
                'details': 'La página no tiene meta descripción'
            }
        
        desc_text = meta_desc.get('content').strip()
        length = len(desc_text)
        
        if 150 <= length <= 160:
            return {
                'passed': True,
                'score': 100,
                'message': f'Meta descripción óptima ({length} caracteres)',
                'details': f'"{desc_text}"'
            }
        elif 120 <= length <= 180:
            return {
                'passed': True,
                'score': 80,
                'message': f'Meta descripción aceptable ({length} caracteres)',
                'details': f'"{desc_text}"'
            }
        else:
            return {
                'passed': False,
                'score': 30,
                'message': f'Meta descripción subóptima ({length} caracteres)',
                'details': f'"{desc_text}" - Recomendado: 150-160 caracteres'
            }

    def _check_h1_tag(self, soup):
        h1_tags = soup.find_all('h1')
        
        if len(h1_tags) == 0:
            return {
                'passed': False,
                'score': 0,
                'message': 'No se encontró etiqueta H1',
                'details': 'La página debe tener exactamente una etiqueta H1'
            }
        elif len(h1_tags) == 1:
            h1_text = h1_tags[0].get_text().strip()
            return {
                'passed': True,
                'score': 100,
                'message': 'Etiqueta H1 correcta',
                'details': f'H1: "{h1_text}"'
            }
        else:
            return {
                'passed': False,
                'score': 40,
                'message': f'Múltiples etiquetas H1 ({len(h1_tags)})',
                'details': 'Se recomienda usar solo una etiqueta H1 por página'
            }

    def _check_heading_structure(self, soup):
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if len(headings) < 2:
            return {
                'passed': False,
                'score': 20,
                'message': 'Estructura de encabezados insuficiente',
                'details': f'Solo {len(headings)} encabezados encontrados'
            }
        
        structure = {}
        for heading in headings:
            level = heading.name
            structure[level] = structure.get(level, 0) + 1
        
        return {
            'passed': True,
            'score': 100,
            'message': 'Buena estructura de encabezados',
            'details': f'Estructura: {structure}'
        }

    def _check_images_alt(self, soup):
        images = soup.find_all('img')
        if len(images) == 0:
            return {
                'passed': True,
                'score': 100,
                'message': 'No hay imágenes en la página',
                'details': 'N/A'
            }
        
        images_with_alt = [img for img in images if img.get('alt')]
        percentage = (len(images_with_alt) / len(images)) * 100
        
        if percentage == 100:
            return {
                'passed': True,
                'score': 100,
                'message': f'Todas las imágenes tienen alt ({len(images)})',
                'details': f'{len(images_with_alt)}/{len(images)} imágenes con texto alternativo'
            }
        elif percentage >= 80:
            return {
                'passed': True,
                'score': 80,
                'message': f'Mayoría de imágenes tienen alt ({percentage:.1f}%)',
                'details': f'{len(images_with_alt)}/{len(images)} imágenes con texto alternativo'
            }
        else:
            return {
                'passed': False,
                'score': int(percentage),
                'message': f'Pocas imágenes con alt ({percentage:.1f}%)',
                'details': f'{len(images_with_alt)}/{len(images)} imágenes con texto alternativo'
            }

    def _check_internal_links(self, soup, url):
        domain = urlparse(url).netloc
        all_links = soup.find_all('a', href=True)
        internal_links = []
        
        for link in all_links:
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                if urlparse(full_url).netloc == domain and href != '#':
                    internal_links.append(href)
        
        count = len(internal_links)
        if count >= 5:
            return {
                'passed': True,
                'score': 100,
                'message': f'Buenos enlaces internos ({count})',
                'details': f'{count} enlaces internos encontrados'
            }
        elif count >= 2:
            return {
                'passed': True,
                'score': 70,
                'message': f'Enlaces internos aceptables ({count})',
                'details': f'{count} enlaces internos encontrados'
            }
        else:
            return {
                'passed': False,
                'score': 20,
                'message': f'Pocos enlaces internos ({count})',
                'details': f'Solo {count} enlaces internos. Recomendado: 5 o más'
            }

    def _check_external_links(self, soup, url):
        domain = urlparse(url).netloc
        all_links = soup.find_all('a', href=True)
        external_links = []
        
        for link in all_links:
            href = link.get('href')
            if href and href.startswith('http'):
                if urlparse(href).netloc != domain:
                    external_links.append(href)
        
        count = len(external_links)
        return {
            'passed': count > 0,
            'score': min(100, count * 20),
            'message': f'Enlaces externos: {count}',
            'details': f'{count} enlaces hacia sitios externos'
        }

    def _check_https(self, url):
        is_https = url.startswith('https://')
        return {
            'passed': is_https,
            'score': 100 if is_https else 0,
            'message': 'HTTPS activado' if is_https else 'HTTPS no activado',
            'details': 'Sitio seguro con SSL' if is_https else 'El sitio no usa protocolo seguro'
        }

    def _check_mobile_viewport(self, soup):
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport and viewport.get('content'):
            content = viewport.get('content')
            return {
                'passed': True,
                'score': 100,
                'message': 'Viewport configurado',
                'details': f'content="{content}"'
            }
        else:
            return {
                'passed': False,
                'score': 0,
                'message': 'Viewport no configurado',
                'details': 'Falta meta tag viewport para optimización móvil'
            }

    def _check_page_speed(self, load_time):
        if load_time <= 2:
            return {
                'passed': True,
                'score': 100,
                'message': f'Velocidad excelente ({load_time:.2f}s)',
                'details': 'Tiempo de carga óptimo'
            }
        elif load_time <= 4:
            return {
                'passed': True,
                'score': 80,
                'message': f'Velocidad buena ({load_time:.2f}s)',
                'details': 'Tiempo de carga aceptable'
            }
        else:
            return {
                'passed': False,
                'score': 40,
                'message': f'Velocidad lenta ({load_time:.2f}s)',
                'details': 'El sitio carga lentamente, optimizar recomendado'
            }