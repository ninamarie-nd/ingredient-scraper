# Brand Queue — 13-Week Audit Pipeline

This file is the source of truth for which brand gets audited on which date. The scheduled Cowork task reads this file every Mon/Wed/Fri to determine today's brand.

---

## SETUP REQUIRED BEFORE LAUNCH

**Edit the `Week 1 Monday` date below before scheduling the recurring task.**

`Week 1 Monday:` **Monday, May 18, 2026**

Every other date in this file is computed from that anchor. If Week 1 Monday is January 5, 2026, then Week 1 Wednesday is January 7, Week 1 Friday is January 9, Week 2 Monday is January 12, and so on.

---

## How Cowork reads this file

When the scheduled task fires, it should:

1. Get today's date.
2. Confirm today is a Monday, Wednesday, or Friday. If not, stop.
3. Calculate which week and day-slot today corresponds to, using `Week 1 Monday` as the anchor.
4. Look up the brand assigned to that week + slot in the schedule below.
5. If today's date is past Week 13 Friday, stop and notify Nina-Marie that the pipeline is complete.
6. If the brand is already marked `✅ complete`, stop and notify (this prevents accidental re-audits).
7. Otherwise, run the audit using the brand name and URL listed.
8. After the audit completes, edit this file to mark today's entry as `✅ complete`.

---

## The Schedule

Format: each row shows the relative day offset from Week 1 Monday, the brand, and the URL. Status column starts empty; Cowork fills it in.

### Week 1

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +0 | Mon (Curly) | Innersense Organic Beauty | https://innersensebeauty.com | ✅ complete |
| +2 | Wed (Bath) | The Honest Company | https://www.honest.com | ✅ complete |
| +4 | Fri (Skincare) | CeraVe | https://www.cerave.com | ✅ complete |

### Week 2

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +7 | Mon (Curly) | Briogeo | https://briogeohair.com | ✅ complete |
| +9 | Wed (Bath) | SheaMoisture | https://www.sheamoisture.com | ✅ complete |
| +11 | Fri (Skincare) | Drunk Elephant | https://www.drunkelephant.com | ✅ complete |

### Week 3

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +14 | Mon (Curly) | Mielle Organics | https://mielleorganics.com | ✅ complete |
| +16 | Wed (Bath) | Aveeno | https://www.aveeno.com | ✅ complete |
| +18 | Fri (Skincare) | ATTITUDE | https://attitudeliving.com | ✅ complete |

### Week 4

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +21 | Mon (Curly) | Carol's Daughter | https://www.carolsdaughter.com | ✅ complete |
| +23 | Wed (Bath) | Johnson's | https://www.johnsonsbaby.com | ✅ complete |
| +25 | Fri (Skincare) | Bubble Skincare | https://www.bubbleskincare.com | ✅ complete |

### Week 5

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +28 | Mon (Curly) | Pattern Beauty | https://patternbeauty.com | ✅ complete |
| +30 | Wed (Bath) | Hello Bello | https://hellobello.com | ✅ complete |
| +32 | Fri (Skincare) | Native | https://www.nativecos.com | ✅ complete |

### Week 6

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +35 | Mon (Curly) | Cantu | https://www.cantubeauty.com | ✅ complete |
| +37 | Wed (Bath) | Tubby Todd | https://tubbytodd.com | |
| +39 | Fri (Skincare) | Glow Recipe | https://www.glowrecipe.com | |

### Week 7

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +42 | Mon (Curly) | Bounce Curl | https://bouncecurl.com | |
| +44 | Wed (Bath) | Pipette | https://www.pipettebaby.com | |
| +46 | Fri (Skincare) | Pacifica | https://www.pacificabeauty.com | |

### Week 8

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +49 | Mon (Curly) | TGIN (Thank God It's Natural) | https://tginatural.com | |
| +51 | Wed (Bath) | Babo Botanicals | https://babobotanicals.com | |
| +53 | Fri (Skincare) | Sol de Janeiro | https://www.soldejaneiro.com | |

### Week 9

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +56 | Mon (Curly) | Curlsmith | https://curlsmith.com | |
| +58 | Wed (Bath) | Earth Mama | https://earthmamaorganics.com | |
| +60 | Fri (Skincare) | Eos | https://evolutionofsmooth.com | |

### Week 10

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +63 | Mon (Curly) | Adwoa Beauty | https://adwoabeauty.com | |
| +65 | Wed (Bath) | Mustela | https://www.mustelausa.com | |
| +67 | Fri (Skincare) | Beautycounter | https://www.beautycounter.com | |

### Week 11

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +70 | Mon (Curly) | Camille Rose | https://www.camillerose.com | |
| +72 | Wed (Bath) | Frida Baby | https://frida.com | |
| +74 | Fri (Skincare) | Evereden | https://www.evereden.com | |

### Week 12

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +77 | Mon (Curly) | Kinky-Curly | https://kinky-curly.com | |
| +79 | Wed (Bath) | Cetaphil | https://www.cetaphil.com | |
| +81 | Fri (Skincare) | Sincerely Yours | https://sincerelyours.com | |

### Week 13

| Day offset | Slot | Brand | URL | Status |
|---|---|---|---|---|
| +84 | Mon (Curly) | Miss Jessie's | https://www.missjessies.com | |
| +86 | Wed (Bath) | Burt's Bees | https://www.burtsbees.com | |
| +88 | Fri (Skincare) | August | https://www.itsaugust.co | |

---

## Spillover brands (Week 14+ or quarterly re-audits)

These don't have scheduled dates. Run manually when ready.

| Brand | URL | Status |
|---|---|---|
| Aussie Miracle Curls | https://www.aussie.com | not scheduled |
| DevaCurl | https://www.devacurl.com | not scheduled |

---

## Progress tracker

This section gets updated automatically as audits complete.

- **Total brands in pipeline:** 39
- **Completed:** 16
- **Remaining:** 23
- **Last audit completed:** Cantu — 2026-10-15 (Week 6 Monday, resumed post-pipeline)
- **Next scheduled audit:** pipeline window closed 2026-08-14; next brand to resume is Week 6 Wednesday — Tubby Todd. On 2026-10-15, five brands caught up: Johnson's, Pattern Beauty, Hello Bello, Native, Cantu.

---

## Manual override instructions

If Nina-Marie needs to:

- **Skip a week** (e.g., vacation, illness): edit each brand's status in that week to `⏭ skipped — rescheduled to [date]` and add the brand to the next available slot below Week 13.
- **Reorder brands:** edit the brand names in the table directly. The day offsets stay anchored to dates, not brands.
- **Swap a brand:** replace the brand name and URL in the row. Don't change the day offset.
- **Pause the pipeline:** in Cowork, disable the recurring task. The queue stays intact; just won't fire.
- **Re-audit a completed brand:** clear its status from `✅ complete` back to empty, and Cowork will treat it as the next audit on a matching day.

---

## End-of-pipeline behavior

When Cowork hits a day where today's date is past Week 13 Friday (day offset +88), it should:

1. Stop attempting to audit.
2. Post a completion summary: "All 39 brands in the pipeline have been audited. Total time: X weeks. Outputs are in audits/. Spillover brands available: Aussie Miracle Curls, DevaCurl. Want to start a re-audit cycle, audit the spillover brands, or pause?"
3. Wait for Nina-Marie's direction.
