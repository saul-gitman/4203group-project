# Sources and facts

Facts used in the deck, with where they come from. Accessed November 2026.

## Hong Kong law and trials

| fact | source |
|---|---|
| Small Unmanned Aircraft Order (Cap. 448G) in full effect 1 Dec 2022 | [CAD AC-013](https://www.cad.gov.hk/documents/AC-013.pdf) |
| From 18 Jul 2025, Cap. 448G covers 25–150 kg (Category C, needs CAD permission) | [HKSAR Gov press release, 17 Jul 2025](https://www.info.gov.hk/gia/general/202507/17/P2025071700590.htm); [LegCo CB(3)888/2025(06)](https://www.legco.gov.hk/yr2025/chinese/hc/sub_leg/sc101/papers/sc10120250609cb3-888-6-ce.pdf) |
| Cap. 448C amendment lets the Chief Executive permit trials of unconventional aircraft (>150 kg unmanned, powered-lift, multicopter); the DGCA exercises the power | press release above; [AIC 20/25](https://www.ais.gov.hk/HKAIP/aic/AIC20-25.pdf) ¶1.2, ¶2.1 |
| Trial aircraft must stay inside the accepted operating area at all times; route planning must account for navigation accuracy, DAA and latency | AIC 20/25 ¶5.3–5.4 |
| GNSS signal integrity adequate across the area; avoid dense high-rise districts; procedures for degraded GNSS | AIC 20/25 ¶5.5, ¶4.4(d), ¶11.1(d) |
| Autonomous operation prohibited except pre-programmed emergency actions | AIC 20/25 ¶6.10 |
| First Sandbox: 38 projects picked from 72 applications | [TLB Sandbox page](https://www.tlb.gov.hk/eng/highlights/transport/low-altitude.html) |
| Sandbox X launched 24 Nov 2025 (cross-boundary drones, passenger aircraft, platforms) | [news.gov.hk](https://www.news.gov.hk/eng/2025/11/20251124/20251124_212226_301.html) |

## EH216-S

| fact | source |
|---|---|
| CAAC type certificate, Oct 2023 | [AAM International](https://aaminternational.com/2023/10/ehang-obtains-type-certificate-for-eh216-s) |
| Standard airworthiness certificate, Dec 2023 | [Asian Aviation](https://asianaviation.com/posts/eh216-s-uav-system-gains-caac-airworthiness-certificate) |
| Production certificate, Apr 2024 | [CompositesWorld](https://compositesworld.com/news/ehang-secures-production-certification-from-caac) |
| Air operator certificates to EHang General Aviation and Heyi Aviation, 2025 | [Business Aviation](https://businessaviation.aero/evtol-news-and-electric-aircraft-news/advanced-air-mobility/ehang-receives-air-operator-certificates-for-its-eh216-s) |
| First public HK flight, Cyberport, 28 Aug 2026, under Sandbox X | [avi-go](https://avi-go.com/news/articles/0f04e4bfd9d30749962cbc829c09eb32) |

## Singapore

| fact | source |
|---|---|
| Class 2 Activity Permit above 200 ft AMSL, within 5 km of any aerodrome/airbase, or in restricted/danger areas; Operator Permit holders use CFMS + UA tracker | [CAAS permits](https://www.caas.gov.sg/unmanned-aircraft/operator-and-activity-permits/) |
| 18–19 Jun 2019: drone sightings suspended a Changi runway on and off, ~37 flights delayed, 1 diverted | [CAAS](https://www.caas.gov.sg/resources/media-and-publication/newsroom/response-to-media-queries-on-drone-sightings-in-the-vicinity-of-changi-airport/) |
| CAAS picked Thales (with Deeeplabs) for a national UTM system, May 2026 | [Asian Aviation](https://asianaviation.com/posts/thales-to-build-singapores-drone-traffic-management-platform) |
| Volocopter flew over Marina Bay Oct 2019, aimed for 2024 service, insolvent Dec 2024, assets bought by Wanfeng/Diamond | [AVweb](https://avweb.com/aviation-news/diamonds-owner-buys-volocopter/) |

## GNSS incidents in Hong Kong

| fact | source |
|---|---|
| Oct 2018 Wine & Dine show: GPS jamming dropped 46 of 100 drones into Victoria Harbour, ~HK$1M damage | [SCMP](https://www.scmp.com/news/hong-kong/law-and-crime/article/2170669/hk13-million-damage-caused-gps-jamming-caused-46-drones) |
| 30 Sep and 1 Oct 2024 harbour drone shows cancelled for ionospheric scintillation; show drones must hold 5–10 cm | [RTHK](https://news.rthk.hk/rthk/en/component/k2/1772972-20241002.htm), [RTHK](https://news.rthk.hk/rthk/en/component/k2/1772911-20241001.htm) |

## Standards and trends

| fact | source |
|---|---|
| EUROCAE ED-318 (Feb 2024): common digital format for UAS geographical zones | [EUROCAE](https://www.eurocae.net/product/ed-318-technical-specification-for-geographical-zones-and-u-space-data-provision-and-exchange/) |
| DJI turned US no-fly zones into warnings, 13 Jan 2025 | [DroneDJ](https://dronedj.com/2025/01/14/dji-geofencing-no-fly-zone/) |
| China GB 42590-2023, first mandatory civil-drone standard, in force 1 Jun 2024 | [notice](https://zrlklab.com/en/show-99-2690.html) |
| SORA 2.5 evaluates containment at Step 8 | [JARUS SORA 2.5 Main Body](https://www.caa.cz/wp-content/uploads/2024/12/SORA-v2.5-Main-Body-Release-JAR_doc_25.pdf) |

## Papers (IEEE, as on slide 23)

1. L.-T. Hsu, F. Huang, H.-F. Ng, G. Zhang, Y. Zhong, X. Bai and W. Wen, "Hong Kong UrbanNav: An open-source multisensory dataset for benchmarking urban navigation algorithms," *NAVIGATION*, vol. 70, no. 4, navi.602, 2023. [doi](https://doi.org/10.33012/navi.602)
2. J. A. Klobuchar, "Ionospheric time-delay algorithm for single-frequency GPS users," *IEEE Trans. Aerosp. Electron. Syst.*, vol. AES-23, no. 3, pp. 325–331, 1987. (Cited from memory; check volume and pages.)
3. H.-F. Ng, "Urban navigation using 3D mapping-aided (3DMA) GNSS," Ph.D. thesis, PolyU AAE, 2025. [pdf](https://theses.lib.polyu.edu.hk/bitstream/200/13662/3/8104.pdf)

## Own results (simulated, this repo)

| fact | how to reproduce |
|---|---|
| With R + k·σ_h: 0 of 80 flights within 3 m of the zone. Without: 76 of 80 | `python code/analysis/baseline.py` |
| Flight 1 brakes, holds 15.1 m from the zone; flight 2 turns 98 m out, passes the tower 16.2 m clear | `python code/main.py`, `python code/analysis/trajectories.py` |
| Brake vs turn crossover v = √(2aR) = 15.8 m/s | `python code/params.py` |
