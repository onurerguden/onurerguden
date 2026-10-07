# Profile visuals

The profile follows the portfolio palette: navy, ice blue and lime, with readable light-mode variants and native technology logo colors. All displayed SVGs live in this repository.

The static engineering drawing has separate wide (900 × 96) and narrow (450 × 96) compositions. Names, the professional title, project descriptions and links remain selectable Markdown text.

## Automated assets

`.github/workflows/profile-visuals.yml` refreshes the stats, language cards and contribution snake daily at 03:17 UTC (06:17 in Türkiye). It can also be run manually from Actions.

- [GitHub Stats Extended](https://github.com/stats-organization/github-stats-extended) through [GitHub Readme Stats Action](https://github.com/stats-organization/github-readme-stats-action).
- [Platane/snk](https://github.com/Platane/snk) for the contribution snake.
- `scripts/prepare_snake.py` decorates the generated route with direction-aware eyes, a forked tongue, a small eating reaction and bounded body growth. It retains reduced-motion support.

Actions are pinned to commit SHAs; the stats core is pinned to 2.2.1. The workflow uses the built-in repository token and no additional secrets. It fails on a stats-fetch error so that the last successful cards remain available. Generated assets do not trigger another run.

`scripts/prepare_cards.py` derives 330 × 180 narrow cards from the same generated values without another API call. On small screens the text remains readable rather than scaling a wide layout down.

The stats card labels its commit period. PR and star totals are cumulative. The language card measures code size in public, non-fork repositories, excluding this profile's generated SVGs. It is not a measure of proficiency or hours spent coding. These cards do not expose private repository details.

## Snake behavior

The original contribution grid, clearing times and route come from the pinned Platane generator. Its collection/progress bar is removed. The decorator reads the head keyframes and cell-clearing events, then builds overlapping trailing body pieces on the same path. The body starts at roughly four cells long and gradually grows to at most twelve; growth is a visual interpretation, not a change to the upstream path-finding solver. A cell consumption lights a subtle ring at that cell. The character uses a pastel green, flat rounded head and simple dot eyes, without a mouth or a chewing animation. The face turns with the route and a small tongue flicks periodically. The loop resets its growth during the return path. With reduced motion, the graph and a short, still snake remain visible while flashes and the tongue are hidden.

If the expected upstream SVG structure changes, decoration fails rather than silently producing a broken animation; the workflow retains the last successful assets.

## Technology badges and connections

The profile uses local, readable SVG badges with brand colors and [Simple Icons](https://github.com/simple-icons/simple-icons) 16.34.0 where available. Simple generic symbols cover tools without an available brand icon. Its license is included in `assets/badges/SIMPLE-ICONS-LICENSE`. Earlier Skill Icons assets retain their MIT license in `assets/tech/LICENSE`.

The [full technology inventory](technology-inventory.md) is a dated snapshot of accessible personal and organization repositories, dependency manifests, import statements, and the published portfolio/CV. Private project names, files, code and credentials stay out of this repository. This inventory is separate from the daily public-repository language widget.

Connect with me links are verified against the published site/GitHub profile or supplied directly by the profile owner. The Instagram account was supplied directly. The profile views badge uses [GitHub Profile Views Counter](https://github.com/antonkomarev/github-profile-views-counter); it counts image/page requests, not unique people or historic visits. No artificial base count is added.

## References

- [Average to PRO GitHub Profile](https://www.youtube.com/watch?v=Qng4TaXP904)
- [Snake Game on GitHub Profile](https://www.youtube.com/watch?v=U-IVndCqXWc)
- [GitHub's profile guide for job seekers](https://docs.github.com/en/account-and-profile/tutorials/using-your-github-profile-to-enhance-your-resume)
