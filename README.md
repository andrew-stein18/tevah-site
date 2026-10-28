# tevah.io

The Tevah landing page: a dithered ark that rises out of the flood.

- `site/`: the deployable static site (`index.html` is fully self-contained), hosted on Vercel.
- `source/site.template.html`: the page source. `source/bg_layers.json` holds the dithered scene data.
- `source/build_site.py`: injects the scene into the template and writes `site/`.
- `brand/`: wordmark and icon.

```bash
python3 source/build_site.py
cd site && vercel deploy --prod
```
