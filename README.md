# mdrafiislam.github.io

Personal website of Md Rafi Islam, hosted free on GitHub Pages.

## What is in this folder

| Path | What it is |
|---|---|
| `index.html` | The whole website: text, layout and styling in one file |
| `assets/rafi.jpg` | Portrait photo |
| `cv/Md_Rafi_Islam_Resume_Industry.pdf` | Industry résumé (2 pages), linked from the site |
| `cv/Md_Rafi_Islam_CV_Academic.pdf` | Academic CV, linked from the site |
| `data/citations.json` | Google Scholar numbers shown on the site |
| `scripts/update_citations.py` | Refreshes `citations.json` from Google Scholar |
| `.github/workflows/update-citations.yml` | Runs that script once a day on GitHub's servers |

## Common edits

- **Change any text:** open `index.html` on GitHub, click the pencil icon, use Ctrl+F to find the sentence, edit it, then click **Commit changes**. The site updates within a minute or two.
- **Replace a CV:** open the `cv` folder, click **Add file > Upload files**, and upload the new PDF with exactly the same file name. It replaces the old one.
- **Replace the photo:** upload a new square JPG to `assets` named `rafi.jpg`.

## Citation numbers

Every day at about 5 am Central, the workflow fetches your public Google Scholar
profile once and saves the citation count, h-index and i10-index to
`data/citations.json`. The website reads that file and shows the date it was last updated.

Scholar does not offer an official API and sometimes refuses automated requests.
When that happens, the workflow logs a warning, changes nothing, and the site keeps
showing the last good numbers with their date. To refresh by hand, go to the
**Actions** tab, choose **Update Scholar citations**, and click **Run workflow**.

GitHub pauses scheduled workflows in a repository with no activity for 60 days.
Each successful daily run counts as activity. If the workflow is ever paused,
GitHub emails you, and you can switch it back on from the Actions tab.
