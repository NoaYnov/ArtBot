import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import mimetypes

def get_extension(response, default='.jpg'):
    content_type = response.headers.get('Content-Type', '').split(';')[0]
    ext = mimetypes.guess_extension(content_type)
    return ext if ext else default

def scrape_images(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://unsplash.com/'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    img_urls = []
    for img in img_tags:
        srcset = img.get('srcset')
        if srcset:
            candidates = [s.strip().split(' ')[0] for s in srcset.split(',')]
            if candidates:
                img_urls.append(candidates[-1])  # version haute résolution
        elif img.get('src'):
            img_urls.append(urljoin(url, img['src']))
    return img_urls

def download_images(img_urls):
    folder_path = 'imgs'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://unsplash.com/'
    }

    for i, img_url in enumerate(img_urls):
        try:
            response = requests.get(img_url, headers=headers, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    ext = get_extension(response)
                    filename = os.path.join(folder_path, f'img{ext}')
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"Téléchargé : {filename}")
                else:
                    print(f"Contenu non image ignoré : {img_url}")
            else:
                print(f"Échec du téléchargement ({response.status_code}): {img_url}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de {img_url}: {e}")

def total_fetch():
    try:
        index = int(input("Indice de l'image à télécharger (1 = première) : "))
        if index < 1:
            print("L’indice doit être ≥ 1.")
            return
    except ValueError:
        print("Entrée invalide. Entrez un nombre entier.")
        return

    url = 'https://unsplash.com/fr'
    all_img_urls = scrape_images(url)

    if len(all_img_urls) >= index:
        selected_img_url = [all_img_urls[index - 1]]
        print(f"Image {index} sélectionnée.")
        download_images(selected_img_url)
        print("Téléchargement terminé.")
    else:
        print(f"Il n'y a que {len(all_img_urls)} images disponibles sur la page.")

def main():
    total_fetch()

if __name__ == "__main__":
    main()
