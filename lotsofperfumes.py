from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, Base, TopSelections, User

# Create database
engine = create_engine('sqlite:///catalog.db')
# Binding the engine to the metadata of the Base class to be accessed
# by declaratives through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# create an instance of DBSession() to establish all conversations with
# the database and represents a "staging zone" for all the objects loaded
# into the database session object.
session = DBSession()

# Create a dummy user
user1 = User(name="Heba Ahmad", email="hebaahmadms@gmail.com")
session.add(user1)
session.commit()

# Create Categories of Citrus Perfume
fragrance1 = Categories(user=user1, name='Citrus', intro="Infused with the \
tangy essence of citrus fruits, these perfumes are a lively and \
energetic bunch. Well-suited to daytime wear, they are just the thing to \
wake you up in the morning before you've had that second cup of coffee")
session.add(fragrance1)
session.commit()

# Add some perfumes' selections into Citrus perfumes' categories
favorite1_1 = TopSelections(
    user=user1, name="Maison Francis Kurkdjian", description="The maker of \
    this exquisite perfume is known for some \
    of the most gorgeous fragrances on the market today including Elizabeth \
    Arden Green Tea, Elie Saab Le Parfum, Jean Paul Gaultier Le Male. This \
    is his signature blend, which is a mix of floral and citrus scents, and \
    much beloved since its debut.", category=fragrance1)
session.add(favorite1_1)
session.commit()

favorite1_2 = TopSelections(
    user=user1, name="Happy by Clinique for Women", description="This fresh \
    and summery scent is a fabulous staple for your \
    perfume wardrobe. Mandarin orange and pink grapefruit blend with \
    crisp floral notes for an airy, feminine fragrance.", category=fragrance1)
session.add(favorite1_2)
session.commit()

favorite1_3 = TopSelections(
    user=user1, name="Burberry Weekend for Women", description="Like \
    Burberry's iconic trench coat, this scent goes with \
    everything. Sparkling nectarine and green sap are layered over floral \
    notes for a fragrance that's fun, modern and \
    youthful.", category=fragrance1)
session.add(favorite1_3)
session.commit()

favorite1_4 = TopSelections(
    user=user1, name="Jo Malone Grapefruit", description="This refreshing \
    scent is a great wake-you-upper. Strong top \
    notes of grapefruit and tangerine announce the perfume, which mellows \
    over time into a fresh linen scent. ", category=fragrance1)
session.add(favorite1_4)
session.commit()

favorite1_5 = TopSelections(
    user=user1, name="CK One by Calvin Klein", description="One of the first \
    successful unisex fragrances, CK One \
    awakens the senses with notes of papaya, pineapple, \
    lemon and floral notes, over a base accord of green tea. A \
    refreshing, clean scent that's light \
    enough to wear to breakfast.", category=fragrance1)
session.add(favorite1_5)
session.commit()

# Create Categories of Floral Perfume
fragrance2 = Categories(
    user=user1, name='Floral', intro="Sweet and romantic, \
    these scents are the 'good girls' of the fragrance aisle. \
    Florals are sometimes single note, but generally, combine the scents of \
    various flowers to create a classic feminine appeal. Spritz on a floral \
    when you want to show off your sweet-and-girly side; when meeting your \
    friend's parents, these scents are also appropriate for special occasions \
    like your best friend's wedding")
session.add(fragrance2)
session.commit()

# Add some perfumes' selections into Floral perfumes' categories
favorite2_1 = TopSelections(
    user=user1, name="No. 5 by Chanel for Women", description="A blend of \
    luxurious florals and warm base notes, \
    including ylang-ylang, rose, iris, neroli and \
    vanilla, No. 5 is an elegant, womanly scent that \
    transitions well from day to nighttime wear.", category=fragrance2)
session.add(favorite2_1)
session.commit()

favorite2_2 = TopSelections(user=user1, name="Chloe by Karl Lagerfield for \
Women", description="Chloe was created by Karl Lagerfeld when he helmed the \
fashion house of Chloe, this fragrance is rich, romantic and powerful. \
Jasmine and honeysuckle are layered over spices and woods, to create a \
fragrance that is boldly feminine.", category=fragrance2)
session.add(favorite2_2)
session.commit()

favorite2_3 = TopSelections(
    user=user1, name="Tresor by Lancome for Women", description="Tresor is a \
    deeply romantic fragrance. Lush and unabashedly floral, with \
    pretty top notes of lilac and apricot, this is \
    an intensely feminine perfume that charms more \
    than it seduces.", category=fragrance2)
session.add(favorite2_3)
session.commit()

favorite2_4 = TopSelections(
    user=user1, name="Flight of Fancy by Anna Sui", description="Like the \
    name suggests, this is a whimsical fragrance that \
    doesn't demand to be taken too seriously. A quirky cocktail of \
    floral and fruity aromas, the perfume appeals with notes of litchi, \
    magnolia, rose and freesia. It's fresh and fun, right down to its \
    peacock-adorned bottle.", category=fragrance2)
session.add(favorite2_4)
session.commit()

favorite2_5 = TopSelections(user=user1, name="Curve by Liz Claiborne \
    for Women", description="Another fruity floral, Curve blends \
    soft floral notes of lily and rose with yummy peach, citrus and \
    berry aromas. This is a crisp, clean perfume that's best-suited \
    to daytime wear.", category=fragrance2)
session.add(favorite2_5)
session.commit()

# Create Categories of Fruity Perfume
fragrance3 = Categories(user=user1, name='Fruity', intro="Like a cheerleader \
with a wicked side, fruity perfumes are fresh and spicy. These fragrances \
please the nose with the bright and familiar smells of apple, peach, berry, \
mango and other juicy fruits, often blended with \
florals to create a compelling aroma.")
session.add(fragrance3)
session.commit()

# Add some perfumes' selections into Fruity perfumes' categories
favorite3_1 = TopSelections(
    user=user1, name="Liz Claiborne by Liz Claiborne",
    description="--", category=fragrance3)
session.add(favorite3_1)
session.commit()

favorite3_2 = TopSelections(
    user=user1, name="Avon Fire Me Up", description="--", category=fragrance3)
session.add(favorite3_2)
session.commit()

favorite3_3 = TopSelections(
    user=user1, name="Harajuku Lovers Lil' Ange",
    description="--", category=fragrance3)
session.add(favorite3_3)
session.commit()

favorite3_4 = TopSelections(user=user1, name="Ralph \
    Lauren Ralph Wild", description="--", category=fragrance3)
session.add(favorite3_4)
session.commit()

favorite3_5 = TopSelections(
    user=user1, name="Marc Jacobs Splash: Apple 2010",
    description="--", category=fragrance3)
session.add(favorite3_5)
session.commit()

# Create Categories of Green or Fresh Perfume
fragrance4 = Categories(
    user=user1, name='Green', intro="Smelling of fresh leaves and newly-mown \
    grass, the green fragrances are a natural and energetic \
    group. These scents tend toward the unisex, so are best left on the shelf \
    when you're dressing. Save them for daytime, great fit for any \
    casual or outdoor gathering.")
session.add(fragrance4)
session.commit()

# Add some perfumes' selections into Green or Fresh perfumes' categories
favorite4_1 = TopSelections(
    user=user1, name="No. 19 Perfume for Women by Chanel", description="This \
    fragrance is boldly unique, right down to its \
    signature greenish tint. It successfully blends green and floral \
    notes over a base of moss and woods, evoking a rain-soaked \
    forest. Not girlish or obvious in the least, this is a chic, \
    grown-up scent for a woman who \
    is confident in her femininity.", category=fragrance4)
session.add(favorite4_1)
session.commit()

favorite4_2 = TopSelections(
    user=user1, name="Miss Dior Perfume for Women by \
    Dior", description="Miss Dior was the first scent from the legendary \
    designer Christian Dior, and its timeless appeal has made it a top-seller \
    for six decades.The perfume opens with crisp \
    green sage, with floral notes and a sexy base of leather and \
    patchouli adding complexity.",
    category=fragrance4)
session.add(favorite4_2)
session.commit()

favorite4_3 = TopSelections(
    user=user1, name="Safari Perfume for Women by \
    Ralph Lauren", description="Ralph Lauren was inspired to create \
    the warm and feminine Safari by his travels to the African plains. Its \
    pervasive mossy-green aroma is warmed by rich vanilla and floral notes, \
    giving it a girl-next-door-lets-her-hair-down charm.", category=fragrance4)
session.add(favorite4_3)
session.commit()

favorite4_4 = TopSelections(
    user=user1, name="Sung Alfred Sung", description="Another green-floral \
    blend, Alfred Sung's classic perfume for women evokes the scents of \
    a wedding bouquet. Bright green notes combine \
    with fresh white flowers, with a vanilla-woods base supplying warmth and \
    depth. Very feminine and beautifully balanced in its \
    composition", category=fragrance4)
session.add(favorite4_4)
session.commit()

favorite4_5 = TopSelections(
    user=user1, name="--",
    description="--", category=fragrance4)
session.add(favorite4_5)
session.commit()

# Create Categories of Oceanic Perfumes
fragrance5 = Categories(user=user1, name='Oceanic', intro="Oceanic \
perfumes are a modern invention, first appearing with Christian Dior's \
Dune in 1991. These scents use a blend of synthetic compounds to evoke \
natural aromas such as mountain air, ocean spray or clean linen. Crisp \
and fresh, they are an ideal choice for job interviews.")
session.add(fragrance5)
session.commit()

# Add some perfumes' selections into Oceanic perfumes' categories
favorite5_1 = TopSelections(user=user1, name="Giorgio Beverly Hills Ocean \
Dream for Women", description="Giorgio's Ocean Dream is a feminine \
take on the oceanic category. Evoking romance at the beach, with its blend \
of water plants and floral notes over a warm base of vanilla and \
musk, this is a sensual and feminine perfume that's great for a daytime \
date.", category=fragrance5)
session.add(favorite5_1)
session.commit()

favorite5_2 = TopSelections(user=user1, name="L'Eau par Kenzo by Kenzo for \
Women", description="This fresh and cheerful fragrance is \
like a pair of perfect-fitting jeans. That is, it goes with everything you \
own, and you'll smile every time you put it on. Top notes of reed stems \
and wild mint mingle with freshwater florals and peach, creating a scent \
that's bright, feminine and clean. ", category=fragrance5)
session.add(favorite5_2)
session.commit()

favorite5_3 = TopSelections(
    user=user1, name="Cool Water Woman by Davidoff", description="Refreshing and \
    youthfully sweet, this oceanic-floral combines \
    top notes of ozone and water lily with tropical fruits and berries. \
    The effect is sparkling and young. The water-drop \
    shaped bottle is pretty, too.", category=fragrance5)
session.add(favorite5_3)
session.commit()

favorite5_4 = TopSelections(
    user=user1, name="Sunflowers by Elizabeth Arden \
    for Women", description="While sunflowers could be classified \
    as a fruity-floral, its signature watery scent makes it an \
    oceanic as well. Bright and happy, this is a fabulous mood-boosting \
    fragrance to spritz on first thing in the morning.", category=fragrance5)
session.add(favorite5_4)
session.commit()

favorite5_5 = TopSelections(
    user=user1, name="--", description="--", category=fragrance5)
session.add(favorite5_5)
session.commit()

# Create Categories of Oriental Perfumes
fragrance6 = Categories(user=user1, name='Oriental', intro="Exotic and \
distinctly feminine, these sensual blends feature an earthy, animalistic \
base scent such as musk or ambergris, often combined with warm notes such \
as amber. When combined with florals, these scents are called 'florientals'.")
session.add(fragrance6)
session.commit()

# Add some perfumes' selections into Oriental perfumes' categories
favorite6_1 = TopSelections(
    user=user1, name="Elizabeth Taylor Black Pearls",
    description="--", category=fragrance6)
session.add(favorite6_1)
session.commit()

favorite6_2 = TopSelections(
    user=user1, name="Yves Saint Laurent Opium",
    description="--", category=fragrance6)
session.add(favorite6_2)
session.commit()

favorite6_3 = TopSelections(
    user=user1, name="Guerlain Shalimar",
    description="--", category=fragrance6)
session.add(favorite6_3)
session.commit()

favorite6_4 = TopSelections(
    user=user1, name="Givenchy Organza", description="--", category=fragrance6)
session.add(favorite6_4)
session.commit()

favorite6_5 = TopSelections(
    user=user1, name="Versace Crystal Noir",
    description="--", category=fragrance6)
session.add(favorite6_5)
session.commit()

# Create Categories of Spicy Perfumes
fragrance7 = Categories(
    user=user1, name='Spicy', intro="Sugar and spice and \
    everything nice, that's what these perfumes smell like. With notes of \
    cloves, ginger, cinnamon, cardamom, and pepper, spicy perfumes are \
    comforting and alluring in an old-fashioned way.")
session.add(fragrance7)
session.commit()

# Add some perfumes' selections into Spicy perfumes' categories
favorite7_1 = TopSelections(
    user=user1, name="Miu Miu", description="Its \
    floral and peppery notes make Miu Miu's signature fragrance a great \
    pick for anyone looking for something both sultry and sweet.",
    category=fragrance7)
session.add(favorite7_1)
session.commit()

favorite7_2 = TopSelections(
    user=user1, name="Bond No. 9 Chinatown", description="This perfume has \
    notes of peach blossoms, gardenia, tuberose, \
    patchouli, and cardamom (which is the spice). It is sultry and described \
    as an 'East-West bouquet.'", category=fragrance7)
session.add(favorite7_2)
session.commit()

favorite7_3 = TopSelections(
    user=user1, name="Donna Karan Woman", description="Donna Karan Woman is \
    a blend of Haitian vetiver, sandalwood, and orange blossom - the perfect \
    spicy yet sweet pick.", category=fragrance7)
session.add(favorite7_3)
session.commit()

favorite7_4 = TopSelections(
    user=user1, name="Coco Perfume for Women by Chanel",
    description=" Chanel's complex cocktail of spices and florals is a \
    brilliant blend of sweet and savory notes, including rose, \
    coriander, orange blossom, and cloves, over a deeper, mysterious \
    base of woods and vanilla.", category=fragrance7)
session.add(favorite7_4)
session.commit()

favorite7_5 = TopSelections(
    user=user1, name="Vetyver Cologne by Jo Malone",
    description="Here's a great example of a successful unisex perfume. Jo \
    Malone designed Vetyver to be worn by women and men, and its clean, warm \
    fragrance truly does have universal appeal. Spicy fresh and \
    green, with top notes of tarragon and nutmeg, \
    the scent is reminiscent of both the \
    outdoors and hot, fresh towels. Call it a day trip to \
    the spa in a bottle.", category=fragrance7)
session.add(favorite7_5)
session.commit()

# Create Categories of Woody (Chypre) Perfumes
fragrance8 = Categories(
    user=user1, name='Woody (Chypre)', intro="Woody scents \
    are built on base notes of bark and moss, conjuring winding forest paths. \
    While more unisex than other fragrance categories, that's not to say \
    these scents are masculine. They evoke a particular brand of \
    no-nonsense femininity. Wear one to your next performance review.")
session.add(fragrance8)
session.commit()

# Add some perfumes' selections into Woody perfumes' categories
favorite8_1 = TopSelections(
    user=user1, name="Estee Lauder Knowing",
    description="--", category=fragrance8)
session.add(favorite8_1)
session.commit()

favorite8_2 = TopSelections(
    user=user1, name="Chanel No. 19",
    description="--", category=fragrance8)
session.add(favorite8_2)
session.commit()

favorite8_3 = TopSelections(
    user=user1, name="Britney Spears Believe",
    description="--", category=fragrance8)
session.add(favorite8_3)
session.commit()

favorite8_4 = TopSelections(
    user=user1, name="Ralph Lauren Romance",
    description="--", category=fragrance8)
session.add(favorite8_4)
session.commit()

favorite8_5 = TopSelections(
    user=user1, name="Gucci Envy Me",
    description="--", category=fragrance8)
session.add(favorite8_5)
session.commit()

print "Added Caregories and Perfumes!"
