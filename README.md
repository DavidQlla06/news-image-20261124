# news-image-20261124 — The World in One Page

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/DavidQlla06/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/DavidQlla06/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Entry for the make.fun competition
[news-image-20261124](https://make.fun/bounty/news-image-20261124):
sum up the world's news of Tuesday 24 November 2026 in one image.

## The image

A newspaper front page, drawn entirely in code (`generate.py`, Pillow):

- **Lead story:** Nvidia's board votes unanimously to reinstate Jensen
  Huang as CEO, after President Trump dialled into the board meeting;
  shares jump ~27% in a day.
- **World map** with 13 numbered pins: the Russian corvette sunk off
  Libya, COP31 ending with no deal, NATO meeting after Russian missiles
  hit Poland, the Dymer strike, Abu Dhabi peace talks, Gaza's toxic
  contamination, the Indonesia factory fire, the Hormuz blockade threat,
  the Democrats' 258-seat House majority, the World Chess Championship
  opening in Geneva, the UK hosting the 2035 Women's World Cup, and the
  India–Nepal deals.
- **12 brief cards** (world court on Myanmar, Waymo, Alcaraz, India v New
  Zealand, Modi's AI centre, the Belgium strike, Khartoum, Senegal,
  Estonia, the EU–Indonesia trade deal, BepiColombo, and more) plus a
  6-item ticker.

31 stories in total, all sourced from live news on 24 November 2026.

## Run it

```sh
python3 generate.py   # writes entry.png (1024x1024, deterministic)
python3 main.py       # also copies it to /output/entry.png
```

No network access is needed at run time; `stories.json` holds the day's
news and `generate.py` draws everything from it.

## Licence

MIT — see `LICENSE`.
