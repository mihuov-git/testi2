# Lounaat – valmis GitHub Pages -paketti

Tämä paketti sisältää valmiin staattisen sivuston ja GitHub Actions -workflow'n.

## Tiedostot
- `.github/workflows/pages.yml`
- `scripts/fetch_lunches.py`
- `data/lunches.json`
- `index.html`
- `.nojekyll`
- `.gitignore`

## Tärkein neuvo
Älä vie tätä GitHubiin selaimen drag and dropilla, jos `.github` ei ole aiemmin siirtynyt oikein.
Helpoin ja varmin tapa on käyttää **GitHub Desktopia**.

## Nopeat käyttöönotto-ohjeet
1. Luo GitHubiin uusi tyhjä repo.
2. Pura tämä zip **omaksi kansiokseen** koneellesi.
3. Avaa purettu kansio ja varmista, että siellä näkyy myös `.github`.
4. Lisää kansio GitHub Desktopiin.
5. Publish repository.
6. Avaa GitHubissa `Settings -> Pages` ja valitse sourceksi `GitHub Actions`.
7. Avaa `Actions`-välilehti ja aja workflow kerran käsin.
