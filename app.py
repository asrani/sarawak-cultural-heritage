import json
from html import escape
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ruang • Sarawak Heritage", page_icon="🌿", layout="wide")
TOURISM = "https://www.sarawaktourism.com/web/stories/story-view/ethnicities-of-sarawak"
MUSEUM = "https://museum.sarawak.gov.my/web/home/index/"
# Coordinates represent places only; living traditions are deliberately not mapped.
ENTRIES = [
    dict(id="pua", title="Pua kumbu", community="Iban", category="Craft", icon="🧶", description="Explore Iban woven textiles and the knowledge carried through weaving traditions.", source=TOURISM, prompt="What can a textile tell us about the people who make and use it?"),
    dict(id="sape", title="The sound of the sape", community="Orang Ulu", category="Music", icon="🎵", description="Discover the sape, a traditional Orang Ulu musical instrument, and its place in cultural expression.", source=TOURISM, prompt="Listen to a performance shared by its artist. What do you notice about the melody?"),
    dict(id="keringkam", title="Keringkam embroidery", community="Malay", category="Craft", icon="🪡", description="An introduction to Sarawak's keringkam textile craft. Follow the source to explore its artistic context.", source="https://www.sarawaktourism.com/web/attachment/show/?docid=c0srZjlhS2YvVWdYV3VPTCtvNnpCUT09OjoOdwAogUXcmAjnp5hOvGsn", prompt="How does handwork connect generations of makers?"),
    dict(id="bidayuh", title="Bidayuh cultural expressions", community="Bidayuh", category="Community", icon="🌱", description="Begin learning about Bidayuh communities through the Sarawak Tourism Board's overview of the state's peoples.", source=TOURISM, prompt="Which local voices would you seek out to learn more?"),
    dict(id="melanau", title="Melanau cultural expressions", community="Melanau", category="Community", icon="🌊", description="Explore an introductory account of Melanau heritage, within Sarawak's diverse cultural landscape.", source=TOURISM, prompt="How do place and community shape a living tradition?"),
    dict(id="museum", title="Borneo Cultures Museum", community="Multiple communities", category="Place", icon="🏛️", description="A starting point in Kuching for exploring the cultures and heritage of Borneo through museum collections.", source=MUSEUM, prompt="Choose an object and ask whose story it tells.", lat=1.5520, lon=110.3430, location="Kuching", duration=120),
]
LOOKUP = {e['id']: e for e in ENTRIES}
st.session_state.setdefault("saved", [])
st.markdown('''<style>
.block-container {padding-top:2.4rem;max-width:1250px}
h1,h2,h3 {font-family:Georgia,serif!important;letter-spacing:-.025em}
.hero {background:#243d34;color:#fff8ea;padding:42px;border-radius:18px;margin:16px 0 28px}
.hero h1 {color:#fff8ea;font-size:3.6rem;line-height:1.08;margin:12px 0}
.eyebrow {font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#d6bc86}
.hero p {max-width:640px;color:#e6e6d9;font-size:17px}
.kicker {color:#a85431;font-size:12px;text-transform:uppercase;letter-spacing:2px}
footer {visibility:hidden}
@media(max-width:600px){.hero{padding:24px}.hero h1{font-size:2.5rem}}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🌿 Ruang")
    st.caption("SARAWAK • CULTURAL HERITAGE")
    page = st.radio("Your journey", ["Discover", "Heritage map", "My collection", "Visit planner", "About"], label_visibility="collapsed")
    st.divider()
    st.caption("A small window into living heritage.")
    st.info("Demo content • English\n\nSaved items stay in this browser session. Download your collection to keep it.")


def card(e):
    with st.container(border=True):
        st.markdown(f"<span class='kicker'>{escape(e['category'])} · {escape(e['community'])}</span>", unsafe_allow_html=True)
        st.subheader(f"{e['icon']} {e['title']}")
        st.write(e['description'])
        with st.expander("Explore the story"):
            st.write(e['prompt'])
            st.caption("This introductory entry is not a complete account of the community or tradition.")
            st.link_button("Read the source ↗", e['source'])
        saved = e['id'] in st.session_state.saved
        if st.button("✓ Remove from collection" if saved else "+ Save to collection", key=f"save_{page}_{e['id']}", use_container_width=True):
            if saved:
                st.session_state.saved.remove(e['id'])
            else:
                st.session_state.saved.append(e['id'])
            st.rerun()

if page == "Discover":
    st.caption("RUANG / DISCOVER SARAWAK")
    st.markdown('''<div class="hero"><div class="eyebrow">Stories woven through generations</div><h1>A place for culture.<br>A journey of discovery.</h1><p>Meet the crafts, sounds and communities that shape Sarawak. Explore thoughtfully, follow local voices, and start your own collection.</p></div>''', unsafe_allow_html=True)
    cols = st.columns(3)
    cols[0].metric("Heritage introductions", len(ENTRIES))
    cols[1].metric("Themes to explore", len({e['category'] for e in ENTRIES}))
    cols[2].metric("In your collection", len(st.session_state.saved))
    st.divider()
    st.header("Find your connection")
    c1,c2,c3 = st.columns([2,1,1])
    query = c1.text_input("Search heritage", placeholder="Try weaving, music or Kuching…")
    community = c2.selectbox("Community", ["All"] + sorted({e['community'] for e in ENTRIES}))
    category = c3.selectbox("Theme", ["All"] + sorted({e['category'] for e in ENTRIES}))
    results = [e for e in ENTRIES if (community == "All" or e['community']==community) and (category=="All" or e['category']==category) and query.casefold() in ' '.join(str(v) for v in e.values()).casefold()]
    st.caption(f"{len(results)} introductions • a starter selection, not a complete cultural catalogue")
    if not results:
        st.info("No matching entries. Try another search or choose All in the filters.")
    columns = st.columns(2)
    for i,e in enumerate(results):
        with columns[i%2]: card(e)
elif page == "Heritage map":
    st.title("Heritage, in place")
    st.write("Start with the museum in Kuching. This prototype maps physical places only; traditions belong to communities across many locations.")
    places = [e for e in ENTRIES if 'lat' in e]
    st.map(pd.DataFrame(places)[['lat','lon']], zoom=12)
    for e in places: card(e)
    st.caption("Map coordinates are approximate. Confirm directions through the venue before travelling.")
elif page == "My collection":
    st.title("Your heritage collection")
    saved = [LOOKUP[i] for i in st.session_state.saved]
    if not saved:
        st.info("Your collection is waiting. Save an entry on Discover to begin.")
    else:
        st.download_button("Download collection (JSON)", json.dumps(saved, ensure_ascii=False, indent=2), "sarawak-collection.json", "application/json")
        for e in saved: card(e)
elif page == "Visit planner":
    st.title("Make room for discovery")
    st.write("Create a simple museum visit outline and pair it with a learning theme.")
    day = st.date_input("Visit date")
    theme = st.selectbox("Learning focus", ["Craft", "Music", "Community"])
    hours = st.slider("Time available (hours)", 1, 6, 3)
    st.subheader("Your draft visit")
    st.write(f"**{day.strftime('%d %B %Y')} · Kuching · {hours} hour(s)**")
    st.write("1. Begin at Borneo Cultures Museum.")
    st.write(f"2. Explore displays with a focus on {theme.lower()} and note the communities represented.")
    st.write("3. Reflect on what you learned and follow the museum's recommended resources.")
    st.caption("This is a planning template, not a booking or confirmation of opening hours. Check admission and accessibility with the museum.")
    st.link_button("Check official museum information ↗", MUSEUM)
    text = f"Sarawak heritage visit\nDate: {day}\nLocation: Borneo Cultures Museum, Kuching\nTime available: {hours} hours\nLearning focus: {theme}\nCheck opening hours and admission: {MUSEUM}\n"
    st.download_button("Download visit outline", text, "sarawak-visit.txt")
else:
    st.title("Living heritage, shared with care")
    st.write("Ruang is a Streamlit demonstration for discovering Sarawak's cultural heritage. Its small seed catalogue is introductory and does not represent every community or tradition.")
    st.subheader("Learn from the people who hold the knowledge")
    st.write("Ask before recording or photographing people, performances and cultural objects. Respect restrictions on sacred knowledge, and credit makers and storytellers when sharing their work.")
    st.subheader("Sources and next steps")
    st.link_button("Sarawak Tourism Board — ethnicities overview", TOURISM)
    st.link_button("Sarawak Museum Department", MUSEUM)
    st.write("For a public release, collaborate with community contributors to review descriptions, add consented media, and develop language options. This demo has no accounts, submissions, bookings or persistent database.")
st.divider()
st.caption("RUANG · SARAWAK HERITAGE    /    Explore with curiosity. Share with respect.")
