"""
NCERT Content Ingestion Script — run once before starting the app.
Run: python scripts/ingest_ncert.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.rag.retriever import get_retriever

CLASS9_SCIENCE = [
    {"id":"c9_sci_ch1_1","subject":"science_chemistry","class":"9","chapter":"Matter in Our Surroundings",
     "text":"Matter is anything that occupies space and has mass. Matter exists in three states: solid, liquid, and gas. In a solid, particles are closely packed with strong intermolecular forces. In a liquid, particles can flow but are still close together. In a gas, particles move freely with large spaces between them."},
    {"id":"c9_sci_ch1_2","subject":"science_chemistry","class":"9","chapter":"Matter in Our Surroundings",
     "text":"Evaporation is the process by which a liquid changes into a gas at any temperature below its boiling point. Factors affecting evaporation: surface area, temperature, humidity, and wind speed. Evaporation causes cooling — this is why we sweat."},
    {"id":"c9_sci_ch1_3","subject":"science_chemistry","class":"9","chapter":"Matter in Our Surroundings",
     "text":"Latent heat is the heat energy absorbed or released during a change of state without any change in temperature. Latent heat of fusion: heat needed to convert 1 kg of solid to liquid at its melting point. Latent heat of vaporization: heat needed to convert 1 kg of liquid to gas at its boiling point."},
    {"id":"c9_sci_ch2_1","subject":"science_chemistry","class":"9","chapter":"Is Matter Around Us Pure",
     "text":"A pure substance has a definite composition. Elements and compounds are pure substances. A mixture contains two or more substances mixed together but not chemically combined. Mixtures can be homogeneous (like salt water) or heterogeneous (like sand and water)."},
    {"id":"c9_sci_ch2_2","subject":"science_chemistry","class":"9","chapter":"Is Matter Around Us Pure",
     "text":"Separation methods: filtration separates insoluble solids from liquids. Evaporation separates dissolved solids from liquids. Distillation separates two miscible liquids with different boiling points. Chromatography separates dyes or pigments. Centrifugation separates heavier particles by spinning."},
    {"id":"c9_sci_ch8_1","subject":"science_physics","class":"9","chapter":"Motion",
     "text":"Distance is the total path length traveled by an object. Displacement is the shortest straight-line distance from start to end point with direction. Speed = Distance/Time. Velocity = Displacement/Time. Velocity is a vector quantity (has direction), speed is scalar."},
    {"id":"c9_sci_ch8_2","subject":"science_physics","class":"9","chapter":"Motion",
     "text":"Acceleration is the rate of change of velocity. a = (v-u)/t where v=final velocity, u=initial velocity, t=time. Equations of motion: v = u + at; s = ut + (1/2)at²; v² = u² + 2as. These equations apply when acceleration is uniform (constant)."},
    {"id":"c9_sci_ch8_3","subject":"science_physics","class":"9","chapter":"Motion",
     "text":"A distance-time graph: straight line = uniform speed; curved line = non-uniform speed. The slope gives speed. A velocity-time graph: slope gives acceleration; area under graph gives displacement."},
    {"id":"c9_sci_ch9_1","subject":"science_physics","class":"9","chapter":"Force and Laws of Motion",
     "text":"Newton's First Law of Motion (Law of Inertia): An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an unbalanced external force. Inertia is the tendency of an object to resist change in its state of motion. Heavier objects have more inertia."},
    {"id":"c9_sci_ch9_2","subject":"science_physics","class":"9","chapter":"Force and Laws of Motion",
     "text":"Newton's Second Law: F = ma (Force = mass × acceleration). SI unit of force is Newton (N). 1 Newton = force that gives 1 kg mass an acceleration of 1 m/s²."},
    {"id":"c9_sci_ch9_3","subject":"science_physics","class":"9","chapter":"Force and Laws of Motion",
     "text":"Newton's Third Law: For every action, there is an equal and opposite reaction. A rocket moves forward by expelling gas backward. Action and reaction forces act on different objects."},
    {"id":"c9_sci_ch9_4","subject":"science_physics","class":"9","chapter":"Force and Laws of Motion",
     "text":"Momentum = mass × velocity (p = mv). Law of Conservation of Momentum: total momentum before collision equals total momentum after collision in a closed system with no external forces."},
    {"id":"c9_sci_ch10_1","subject":"science_physics","class":"9","chapter":"Gravitation",
     "text":"Universal Law of Gravitation: F = G(m1×m2)/d². G = 6.674×10⁻¹¹ N m²/kg². Every object attracts every other object with force proportional to product of masses and inversely proportional to square of distance."},
    {"id":"c9_sci_ch10_2","subject":"science_physics","class":"9","chapter":"Gravitation",
     "text":"Weight W = mg where g = 9.8 m/s² on Earth. On Moon, g = 1.63 m/s² so weight on Moon = 1/6 of weight on Earth. Mass remains constant everywhere."},
    {"id":"c9_sci_ch10_3","subject":"science_physics","class":"9","chapter":"Gravitation",
     "text":"Archimedes Principle: buoyant force on an object equals weight of fluid displaced. Objects float when buoyant force ≥ weight."},
    {"id":"c9_sci_ch5_1","subject":"science_biology","class":"9","chapter":"Fundamental Unit of Life",
     "text":"The cell is the fundamental structural and functional unit of life. Robert Hooke first observed cells in 1665. Prokaryotic cells (bacteria) have no membrane-bound nucleus. Eukaryotic cells (plants, animals, fungi) have a membrane-bound nucleus."},
    {"id":"c9_sci_ch5_2","subject":"science_biology","class":"9","chapter":"Fundamental Unit of Life",
     "text":"Plant cells have: cell wall (cellulose), large central vacuole, chloroplasts. Animal cells have: centrosome, smaller vacuoles. Both have: cell membrane, nucleus, mitochondria, ribosomes, endoplasmic reticulum, Golgi apparatus."},
    {"id":"c9_sci_ch5_3","subject":"science_biology","class":"9","chapter":"Fundamental Unit of Life",
     "text":"Osmosis is movement of water molecules from higher to lower concentration through a semipermeable membrane. Hypertonic solution → water leaves (plasmolysis). Hypotonic solution → water enters (turgidity)."},
    {"id":"c9_sci_ch7_1","subject":"science_biology","class":"9","chapter":"Diversity in Living Organisms",
     "text":"Classification hierarchy: Kingdom → Phylum → Class → Order → Family → Genus → Species. The five kingdoms: Monera (bacteria), Protista, Fungi, Plantae, Animalia."},
    {"id":"c9_sci_ch6_1","subject":"science_biology","class":"9","chapter":"Tissues",
     "text":"A tissue is a group of similar cells performing a specific function. Plant tissues: meristematic and permanent. Animal tissues: epithelial, connective (bone, blood), muscular, nervous. Blood is a connective tissue."},
]

CLASS10_SCIENCE = [
    {"id":"c10_sci_ch1_1","subject":"science_chemistry","class":"10","chapter":"Chemical Reactions and Equations",
     "text":"A chemical reaction converts reactants to products. Signs: change in state/color, gas evolution, temperature change, precipitate formation. Types: Combination, Decomposition, Displacement, Double Displacement, Redox."},
    {"id":"c10_sci_ch1_2","subject":"science_chemistry","class":"10","chapter":"Chemical Reactions and Equations",
     "text":"Oxidation = loss of electrons or gain of oxygen. Reduction = gain of electrons or loss of oxygen. Combination: A+B→AB. Decomposition: AB→A+B. Displacement: A+BC→AC+B."},
    {"id":"c10_sci_ch3_1","subject":"science_chemistry","class":"10","chapter":"Metals and Non-metals",
     "text":"Metals are shiny, malleable, ductile, good conductors. Non-metals are dull, brittle, poor conductors. Reactivity series (most to least): K, Na, Ca, Mg, Al, Zn, Fe, Pb, H, Cu, Ag, Au."},
    {"id":"c10_sci_ch4_1","subject":"science_chemistry","class":"10","chapter":"Carbon and Its Compounds",
     "text":"Carbon has 4 valence electrons, forms covalent bonds. Catenation allows long chains. Hydrocarbons: alkanes (CnH2n+2, saturated), alkenes (CnH2n, double bond), alkynes (CnH2n-2, triple bond)."},
    {"id":"c10_sci_ch6_1","subject":"science_biology","class":"10","chapter":"Life Processes",
     "text":"Photosynthesis: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂. Occurs in chloroplasts. Light reaction in thylakoids (ATP, NADPH). Calvin cycle in stroma (glucose). Chlorophyll absorbs red and blue light."},
    {"id":"c10_sci_ch6_2","subject":"science_biology","class":"10","chapter":"Life Processes",
     "text":"Aerobic respiration: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 38 ATP. Anaerobic in yeast: glucose → ethanol + CO₂ + 2 ATP. Anaerobic in muscles: glucose → lactic acid + 2 ATP (causes cramps)."},
    {"id":"c10_sci_ch6_3","subject":"science_biology","class":"10","chapter":"Life Processes",
     "text":"Human digestive system: Mouth (amylase breaks starch) → Oesophagus → Stomach (HCl, pepsin) → Small intestine (bile, pancreatic enzymes, absorption through villi) → Large intestine → Rectum → Anus."},
    {"id":"c10_sci_ch8_1","subject":"science_biology","class":"10","chapter":"Heredity and Evolution",
     "text":"Mendel's Laws: Segregation — alleles separate during gamete formation. Independent Assortment — different genes assort independently. Dominant allele masks recessive. Monohybrid cross Aa × Aa: 3:1 ratio."},
    {"id":"c10_sci_ch8_2","subject":"science_biology","class":"10","chapter":"Heredity and Evolution",
     "text":"DNA double helix: A pairs with T, G pairs with C. DNA replication is semi-conservative. Mutations are changes in DNA sequence."},
    {"id":"c10_sci_ch10_1","subject":"science_physics","class":"10","chapter":"Light Reflection and Refraction",
     "text":"Reflection: angle of incidence = angle of reflection. Mirror formula: 1/v + 1/u = 1/f. Concave mirror converges (torch, shaving mirror). Convex mirror diverges (rear-view mirror, wide field of view)."},
    {"id":"c10_sci_ch10_2","subject":"science_physics","class":"10","chapter":"Light Reflection and Refraction",
     "text":"Refraction: bending of light between media. Snell's Law: n₁sinθ₁ = n₂sinθ₂. Lens formula: 1/v - 1/u = 1/f. Power P = 1/f (Dioptres). Convex lens converges; concave lens diverges."},
    {"id":"c10_sci_ch12_1","subject":"science_physics","class":"10","chapter":"Electricity",
     "text":"Ohm's Law: V = IR. Series circuit: R_total = R1+R2+R3 (same current, voltage divides). Parallel: 1/R = 1/R1+1/R2 (same voltage, current divides)."},
    {"id":"c10_sci_ch12_2","subject":"science_physics","class":"10","chapter":"Electricity",
     "text":"Electric power P = VI = I²R = V²/R (Watts). Energy = Power × Time (kWh). 1 kWh = 3.6×10⁶ J. Joule's heating: H = I²Rt. Used in heaters, bulbs, fuses."},
    {"id":"c10_sci_ch13_1","subject":"science_physics","class":"10","chapter":"Magnetic Effects of Current",
     "text":"Current-carrying conductor creates magnetic field (Oersted). Fleming's Left Hand Rule: force on conductor in magnetic field. Used in electric motors."},
    {"id":"c10_sci_ch13_2","subject":"science_physics","class":"10","chapter":"Magnetic Effects of Current",
     "text":"Electromagnetic induction: changing magnetic field induces current (Faraday's law). Fleming's Right Hand Rule. Used in generators. Transformers step up/step down AC voltage."},
]

MATHEMATICS = [
    {"id":"c9_math_ch1_1","subject":"mathematics","class":"9","chapter":"Number Systems",
     "text":"Real numbers include rational (p/q, q≠0) and irrational (√2, π) numbers. Rational decimals: terminating or non-terminating repeating. Irrational: non-terminating non-repeating."},
    {"id":"c9_math_ch2_1","subject":"mathematics","class":"9","chapter":"Polynomials",
     "text":"Polynomial: aₙxⁿ+...+a₁x+a₀. Degree = highest power. Zero of p(x): value where p(a)=0. Remainder theorem: dividing by (x-a) gives remainder p(a). Factor theorem: (x-a) is factor iff p(a)=0."},
    {"id":"c9_math_ch4_1","subject":"mathematics","class":"9","chapter":"Linear Equations in Two Variables",
     "text":"Linear equation ax+by+c=0: graph is always a straight line. System of two equations: unique solution (intersecting lines), no solution (parallel), infinitely many solutions (coincident lines)."},
    {"id":"c9_math_ch6_1","subject":"mathematics","class":"9","chapter":"Lines and Angles",
     "text":"Vertically opposite angles are equal. Alternate interior angles equal when transversal cuts parallel lines. Co-interior angles supplementary (sum=180°). Triangle angle sum=180°."},
    {"id":"c9_math_ch7_1","subject":"mathematics","class":"9","chapter":"Triangles",
     "text":"Congruence rules: SAS, ASA, AAS, SSS, RHS. Isosceles triangle: angles opposite equal sides are equal."},
    {"id":"c9_math_ch12_1","subject":"mathematics","class":"9","chapter":"Heron's Formula",
     "text":"Heron's formula: Area = √(s(s-a)(s-b)(s-c)) where s=(a+b+c)/2 is semi-perimeter. Used when height is unknown but all sides are known."},
    {"id":"c10_math_ch1_1","subject":"mathematics","class":"10","chapter":"Real Numbers",
     "text":"Fundamental Theorem of Arithmetic: every composite number is a unique product of primes. HCF × LCM = product of two numbers. Euclid's Division Algorithm: a = bq + r where 0 ≤ r < b."},
    {"id":"c10_math_ch2_1","subject":"mathematics","class":"10","chapter":"Polynomials",
     "text":"Quadratic ax²+bx+c with zeroes α,β: α+β = -b/a; αβ = c/a. Cubic ax³+bx²+cx+d with zeroes α,β,γ: α+β+γ = -b/a; αβ+βγ+γα = c/a; αβγ = -d/a."},
    {"id":"c10_math_ch3_1","subject":"mathematics","class":"10","chapter":"Pair of Linear Equations",
     "text":"Solving methods: Substitution, Elimination, Cross-multiplication, Graphical. For a₁x+b₁y+c₁=0 and a₂x+b₂y+c₂=0: a₁/a₂ ≠ b₁/b₂ → unique; a₁/a₂=b₁/b₂=c₁/c₂ → infinite; a₁/a₂=b₁/b₂≠c₁/c₂ → no solution."},
    {"id":"c10_math_ch4_1","subject":"mathematics","class":"10","chapter":"Quadratic Equations",
     "text":"Quadratic ax²+bx+c=0 (a≠0). Quadratic formula: x = (-b ± √(b²-4ac))/2a. Discriminant D=b²-4ac: D>0 → two distinct roots; D=0 → equal roots; D<0 → no real roots."},
    {"id":"c10_math_ch5_1","subject":"mathematics","class":"10","chapter":"Arithmetic Progressions",
     "text":"AP: constant difference d between terms. General term: aₙ = a+(n-1)d. Sum of n terms: Sₙ = n/2[2a+(n-1)d] = n/2[first+last]."},
    {"id":"c10_math_ch6_1","subject":"mathematics","class":"10","chapter":"Triangles Similarity",
     "text":"Similar triangles: same shape, different size. AA criterion. Basic Proportionality Theorem (Thales): line parallel to one side divides other two sides proportionally."},
    {"id":"c10_math_ch8_1","subject":"mathematics","class":"10","chapter":"Introduction to Trigonometry",
     "text":"sinθ=opposite/hypotenuse, cosθ=adjacent/hypotenuse, tanθ=opposite/adjacent. Identities: sin²θ+cos²θ=1; 1+tan²θ=sec²θ. sin30°=1/2, sin45°=1/√2, sin60°=√3/2, sin90°=1."},
    {"id":"c10_math_ch10_1","subject":"mathematics","class":"10","chapter":"Circles",
     "text":"Tangent ⊥ radius at point of tangency. Two tangents from external point are equal. Angle in semicircle=90°. Angle at centre = 2× angle at remaining arc."},
    {"id":"c10_math_ch12_1","subject":"mathematics","class":"10","chapter":"Areas Related to Circles",
     "text":"Area of circle=πr². Circumference=2πr. Sector area=(θ/360)×πr². Arc length=(θ/360)×2πr. Segment area = sector area − triangle area."},
    {"id":"c10_math_ch13_1","subject":"mathematics","class":"10","chapter":"Surface Areas and Volumes",
     "text":"Cube: SA=6a², V=a³. Cuboid: SA=2(lb+bh+lh), V=lbh. Cylinder: TSA=2πr(r+h), V=πr²h. Cone: TSA=πr(r+l), V=(1/3)πr²h. Sphere: SA=4πr², V=(4/3)πr³."},
    {"id":"c10_math_ch14_1","subject":"mathematics","class":"10","chapter":"Statistics",
     "text":"Mean=Σfxᵢ/Σf. Mode=l+((f₁-f₀)/(2f₁-f₀-f₂))×h. Median=l+((n/2-cf)/f)×h. l=lower class limit, f=frequency, h=class size, cf=cumulative frequency."},
    {"id":"c10_math_ch15_1","subject":"mathematics","class":"10","chapter":"Probability",
     "text":"P(E) = favourable outcomes / total outcomes. P(E) between 0 and 1. P(E)+P(not E)=1. Fair coin: P(Head)=1/2. Fair die: P(any number)=1/6."},
]


def main():
    print("🚀 Starting NCERT content ingestion...")
    retriever = get_retriever()
    all_docs = CLASS9_SCIENCE + CLASS10_SCIENCE + MATHEMATICS
    documents = [{"id": d["id"], "text": d["text"],
                  "metadata": {"subject": d["subject"], "class": d["class"],
                               "chapter": d["chapter"], "source": "NCERT"}}
                 for d in all_docs]
    print(f"📚 Ingesting {len(documents)} NCERT content chunks...")
    count = retriever.ingest_batch(documents)
    print(f"✅ Successfully ingested {count} documents into ChromaDB!")
    print(f"📊 Total in database: {retriever.get_stats()['total_documents']}")
    print("🎉 NCERT content ready! You can now start the API and frontend.")


if __name__ == "__main__":
    main()
