import json
import random
import time
from sys import stdout, exit

# 修改print方法 避免某些环境下python执行print 不会去刷新缓存区导致信息第一时间不及时输出
def print_now(content=""):
    print(content)
    stdout.flush()



# 别挂配置数据
gua_data_path = "data.json"

# 别卦数据
gua_data_map = {
    "乾乾":{
        "name":"乾为天",
        "words":"元亨利贞。",
        "white_words":"真不错，这个挂真不错。",
        "picture":"天行健，君子以自强不息。",
        "white_picture":"天道刚健，运行不已。君子观此卦象，从而以天为法，自强不息。"
    },
    "兑乾":{
        "name":"泽天夬",
        "words":"扬于王庭，孚号，有厉。告自邑，不利即戎，利有攸往。",
        "white_words":"王庭里正跳舞作乐。有人呼告：“有敌人来犯。”邑中传来命令：“出击不利，要严阵以待。”筮遇此爻，出外旅行则吉利。",
        "picture":"泽上于天，夬。君子以施禄及下，居德则忌。",
        "white_picture":"上卦为兑，兑为泽；下卦为乾，乾为天，可见泽水上涨，浇灌大地，是夬卦的卦象。君子观此卦象，从而泽惠下施，不敢居功自傲，并以此为忌。"
    },
    "离乾":{
        "name":"火天大有",
        "words":"元亨。",
        "white_words":"昌隆通泰。",
        "picture":"火在天上，大有。君子以遏恶扬善，顺天休命。",
        "white_picture":"火在天上，明烛四方，君子观此卦象，取法于火，洞察善恶，抑恶扬善，从而顺应天命，祈获好运。"
    },
    "震乾":{
        "name":"雷天大壮",
        "words":"利贞。",
        "white_words":"吉利",
        "picture":"雷在天上，大壮。君子以非礼弗履。",
        "white_picture":"天上鸣雷是大壮的卦象。君子观此卦象，以迅雷可畏，礼法森严，从而畏威知惧，唯礼是遵。"
    },
    "巽乾":{
        "name":"风天小畜",
        "words":"亨。密云不雨，自我西郊。",
        "white_words":"吉利。在西郊一带浓云密布，但雨没有下来。",
        "picture":"风行天上，小畜。君子以懿文德。",
        "white_picture":"上卦为巽，巽为风；下卦为乾，乾为天，和风拂地，草木低昂，勃勃滋生，这是小畜的卦象。君子观此卦象，取法催发万物的和风，自励风范，推行德教。"
    },
    "坎乾":{
        "name":"水天需",
        "words":"有孚，光亨，贞吉。利涉大川。",
        "white_words":"抓到俘虏。大吉大利，吉利的卜问。有利于涉水渡河。",
        "picture":"云上于天，需；君子以饮食宴乐。",
        "white_picture":"云浮聚于天上，待时降雨是需卦的卦象。君子观此卦象，可以宴饮安乐，待时而动。"
    },
    "艮乾":{
        "name":"山天大畜",
        "words":"利贞，不家食，吉。利涉大川。",
        "white_words":"吉利的贞兆。不食于家，食于朝廷，吉利。筮遇此卦，有利于涉水渡河。",
        "picture":"天在山中，大畜。君子以多识前言往行，以畜其德。",
        "white_picture":"太阳照耀于山中，万物摄取阳光雨露，各遂其生，这是大畜的卦象。君子观此卦象，从而广泛地了解古人的嘉言善行，来培养自己的德行。"
    },
    "坤乾":{
        "name":"地天泰",
        "words":"小往大来，吉，亨。",
        "white_words":"付出小，收益大，吉祥，顺利。",
        "picture":"天地交，泰；后以财成天地之道，辅相天地之宜，以左右民。",
        "white_picture":"地气上升，乾气下降，为地气居于乾气之上之表象，阴阳二气一升一降，互相交合，顺畅通达。"
    },

    "乾兑":{
        "name":"天泽履",
        "words":"履虎尾，不咥人，亨。",
        "white_words":"踩着虎尾巴，老虎不咬人，吉利。",
        "picture":"上天下泽，履。君子以辨上下，定民志。",
        "white_picture":"上天下泽，尊卑显别，这是履卦的卦象。君子观此卦象，从而分别上下尊卑，使人民循规蹈矩，安份守纪。"
    },
    "兑兑":{
        "name":"兑为泽",
        "words":"亨，利，贞。",
        "white_words":"亨通。吉利的贞卜。",
        "picture":"丽泽，兑。君子以朋友讲习。",
        "white_picture":"两泽相连，两水交流是兑卦的卦象。君子观此卦象，从而广交朋友，讲习探索，推广见闻。"
    },
    "离兑":{
        "name":"火泽睽",
        "words":"小事吉。",
        "white_words":"筮遇此卦，小事吉利。",
        "picture":"上火下泽，睽。君子以同而异。",
        "white_picture":"上火下泽，两相乖离，是睽卦的卦象。君子观此卦象，从而综合万物之所同，分析万物之所异。"
    },
    "震兑":{
        "name":"雷泽归妹",
        "words":"征凶，无攸利。",
        "white_words":"筮遇此爻，出征凶险。无所利。",
        "picture":"泽上有雷，归妹。君子以永终知敝。",
        "white_picture":"泽上雷鸣，雷鸣水动，用以喻男女心动相爱而成眷属。这是归妹卦的卦象。君子观此卦象，从而在长期的婚姻生活中，体察到婚姻的成功与失败。"
    },
    "巽兑":{
        "name":"风泽中孚",
        "words":"豚鱼，吉。利涉大川，利贞。",
        "white_words":"豚鱼献祭，虽物薄但心诚，吉利。并利于涉水过河。这是吉利的贞卜。",
        "picture":"泽上有风，中孚。君子以议狱缓死。",
        "white_picture":"泽上有风，风起波涌。这是中孚的卦象。君子观此卦象，有感于风化邦国，唯德教为先，因而审议讼狱，不轻置重典。"
    },
    "坎兑":{
        "name":"水泽节",
        "words":"亨，苦节不可贞。",
        "white_words":"亨通。如果以节制为苦，其凶吉则不可卜问。",
        "picture":"泽上有水，节。君子以制数度，议德行。",
        "white_picture":"泽中水满，因而须高筑堤防，这是节卦的卦象。君子观此卦象，从而建立政纲制度，确立伦理原则。"
    },
    "艮兑":{
        "name":"山泽损",
        "words":"有孚，元吉，无咎，可贞。利有攸往。曷之用？二簋可用享。",
        "white_words":"筮遇此卦，将有所俘获，大吉大利，没有灾难，是称心的卜问。而且所往将获利。将有人送来两盆食物，可享口福。",
        "picture":"山下有泽，损。君子以征忿窒欲。",
        "white_picture":"山下有泽是损卦的卦象。君子观此卦象，以泽水浸蚀山脚为戒，从而制止其忿怒，杜塞其贪欲。"
    },
    "坤兑":{
        "name":"地泽临",
        "words":"元，亨，利，贞。至于八月有凶。",
        "white_words":"大吉大利，吉利的卜问。到了八月，可能有凶险。",
        "picture":"泽上有地，临。君子以教思无穷，客保民无疆。",
        "white_picture":"堤岸高出大泽，河泽容于大地，这是临卦的卦象。君子观此卦象，君临天下，教化万民，覃恩极虑，保容万民，德业无疆。"
    },

    "乾离":{
        "name":"天火同人",
        "words":"同人于野，亨。利涉大川，利君子贞。",
        "white_words":"聚众于郊外，将行大事，吉利。有利于涉水渡河，有利于君子的卜问。",
        "picture":"天与火，同人；君子以类族辨物。",
        "white_picture":"同人之卦，上卦为乾为天为君王，下卦为离为火为臣民，上乾下离象征君王上情下达，臣民下情上达，君臣意志和同，这是同人的卦象。君子观此卦象，取法于火，明烛天地，照亮幽隐，从而去分析物类，辨明情状。"
    },
    "兑离":{
        "name":"泽火革",
        "words":"己日乃孚。元亨利贞。悔亡。",
        "white_words":"祭祀之日用俘虏作人牲，亨通，吉利的卜问。没有悔恨。",
        "picture":"泽中有火，革。君子以治历明时。",
        "white_picture":"内蒸外煏，水涸草枯，如同水泽之中，大火燃烧，这是革卦的卦象。君子观此卦象，了解到泽水涨落，草木枯荣的周期变化，从而修治历法，明确时令。"
    },
    "离离":{
        "name":"离为火",
        "words":"利贞，亨。畜牝牛，吉。",
        "white_words":"吉利的占问，通泰。饲养母牛，吉利。",
        "picture":"明两作，离。大人以继明照四方。",
        "white_picture":"今朝太阳升，明朝太阳升，相继不停顿，这是离卦的卦象。贵族王公观此卦象，从而以源源不断的光明照临四方。"
    },
    "震离":{
        "name":"雷火丰",
        "words":"亨。王假之，勿忧，宜日中。",
        "white_words":"举行祭祀，君王将亲临宗庙。不要担心，最佳时刻当在正午时分。",
        "picture":"雷电皆至，丰。君子以折狱致刑。",
        "white_picture":"电闪雷鸣，是上天垂示的重大天象，这也是丰卦的卦象。君子观此卦象，有感于电光雷鸣的精明和威严，从而裁断讼狱，施行刑罚。"
    },
    "巽离":{
        "name":"风火家人",
        "words":"利女贞。",
        "white_words":"卜问妇女之事吉利。",
        "picture":"风自火出，家人。君子以言有物，而行有恒。",
        "white_picture":"内火外风，风助火势，火助风威，相辅相成，是家人的卦象。君子观此卦象，从而省悟到言辞须有内容才不致于空洞，德行须持之以恒才能充沛。"
    },
    "坎离":{
        "name":"水火既济",
        "words":"亨，小利贞，初吉终乱。",
        "white_words":"亨通。这是小见吉利的贞卜。起初吉利，最后将发生变故。",
        "picture":"水在火上，既济。君子以思患而预防之。",
        "white_picture":"水上火下，水浇火熄，是既济之卦的卦象。君子观此卦象，从而有备于无患之时，防范于未然之际。"
    },
    "艮离":{
        "name":"山火贲",
        "words":"亨。小利有攸往。",
        "white_words":"通达。有所往则有小利。",
        "picture":"山下有火，贲。君子以明庶政，无敢折狱。",
        "white_picture":"山下有火，火燎群山，这是贲卦的卦象。君子观此卦象，思及猛火燎山，玉石俱焚，草木皆尽，以此为戒，从而明察各项政事，不敢以威猛断狱。"
    },
    "坤离":{
        "name":"地火明夷",
        "words":"利艰贞。",
        "white_words":"卜问艰难之事则利。",
        "picture":"明入地中，明夷。君子以莅众，用晦而明。",
        "white_picture":"太阳没入地中，是明夷的卦象。君子观此卦象，治民理政，不以苛察为明，而是外愚内慧，容物亲众。"
    },

    "乾震":{
        "name":"天雷无妄",
        "words":"元，亨，利，贞。其匪正有眚，不利有攸往。",
        "white_words":"嘉美通泰，卜问得吉兆。行为不正当，则有灾殃，有所往则不利。",
        "picture":"天下雷行，物与无妄。先王以茂对时，育万物。",
        "white_picture":"天宇之下，春雷滚动，万物萌发，孳生繁衍，这是无妄的卦象。先王观此卦象，从而奋勉努力，顺应时令，保育万物。"
    },
    "兑震":{
        "name":"泽雷随",
        "words":"元亨，利贞，无咎。",
        "white_words":"大吉大利，卜得吉兆，没有灾害。",
        "picture":"泽中有雷，随。君子以向晦入宴息。",
        "white_picture":"雷入泽中，大地寒凝，万物蛰伏，是随卦的卦象。君子观此卦象，取法于随天时而沉寂的雷声，随时作息，向晚则入室休息。"
    },
    "离震":{
        "name":"火雷噬嗑",
        "words":"亨。利用狱。",
        "white_words":"通泰。利于讼狱。",
        "picture":"雷电噬嗑。先王以明罚敕法。",
        "white_picture":"雷电交合是噬嗑的卦象。先王观此卦象，取法于威风凛凛的雷、照彻幽隐的电，思以严明治政，从而明察其刑罚，修正其法律。"
    },
    "震震":{
        "name":"震为雷",
        "words":"亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。",
        "white_words":"临祭之时，雷声传来，有的人吓得浑身发抖，片刻之后，才能谈笑如常。巨雷猝响，震惊百里，有的人却神态自若，手里拿着酒勺子，连一滴酒都没有洒出来。",
        "picture":"洊雷，震。君子以恐惧修省。",
        "white_picture":"巨雷连击，是震卦的卦象。君子观此卦象，从而戒惧恐惧，修省其身。"
    },
    "巽震":{
        "name":"风雷益",
        "words":"利有攸往，利涉大川。",
        "white_words":"筮遇此爻，利于有所往，利于涉水渡河。",
        "picture":"风雷，益。君子以见善则迁，有过则改。",
        "white_picture":"风雷激荡，是益卦的卦象。君子观此卦象，惊恐于风雷的威力，从而见善则从之，有过则改之。"
    },
    "坎震":{
        "name":"水雷屯",
        "words":"元，亨，利，贞。勿用，有攸往，利建侯。",
        "white_words":"大吉大利，吉利的占卜。不利于出门。有利于建国封侯。",
        "picture":"云，雷，屯；君子以经纶。",
        "white_picture":"云行于上，雷动于下，是屯卦的卦象。君子观此卦象，取法于云雷，用云的恩泽，雷的威严来治理国事。"
    },
    "艮震":{
        "name":"山雷颐",
        "words":"贞吉。观颐，自求口实。",
        "white_words":"占卜得吉兆。研究颐养之道，在于自食其力。",
        "picture":"山下有雷，颐。君子以慎言语，节饮食。",
        "white_picture":"雷出山中，万物萌发，这是颐卦的卦象。君子观此卦象，思生养之不易，从而谨慎言语，避免灾祸。节制饮食，修身养性。"
    },
    "坤震":{
        "name":"地雷复",
        "words":"亨。出入无疾，朋来无咎。反复其道，七日来复，利有攸往。",
        "white_words":"通泰。出门、居处均无疾病。有钱可赚而可以无灾祸。往返途中，七日可归。有所往则有所利。",
        "picture":"雷在地中，复。先王以至日闭关，商旅不行，后不省方。",
        "white_picture":"天寒地冻，雷返归地中，往而有复，依时回归，这是复卦的卦象。先王观此卦象，取法于雷，在冬至之日关闭城门，不接纳商旅，君王也不巡视邦国"
    },

    "乾巽":{
        "name":"天风姤",
        "words":"女壮，勿用取女。",
        "white_words":"梦见女子受伤。筮遇此卦，不利于娶女。",
        "picture":"天下有风，姤。后以施命诰四方。",
        "white_picture":"天下有风，是姤卦的卦象，君王观此卦象，从而效法于风之吹拂万物，施教化于天下，昭告四方。"
    },
    "兑巽":{
        "name":"泽风大过",
        "words":"栋桡。利有攸往，亨。",
        "white_words":"屋粱压得弯曲了。有所往则有利，通泰。",
        "picture":"泽灭木，大过。君子以独立不惧，遁世无闷。",
        "white_picture":"泽水淹没木舟，这是大过的卦象。君子观此卦象，以舟重则覆为戒，领悟到遭逢祸变，应守节不屈，稳居不仕，清静淡泊。"
    },
    "离巽":{
        "name":"火风鼎",
        "words":"元吉，亨。",
        "white_words":"大吉大利，亨通。",
        "picture":"木上有火，鼎。君子以正位凝命。",
        "white_picture":"木上有火，以鼎烹物，这是《鼎》卦的卦象。君子观此卦象，取法于鼎足三分，正立不倚，从而持正守位，为君上所倚重，不负使命。"
    },
    "雷巽":{
        "name":"雷风恒",
        "words":"亨，无咎，利贞。利有攸往。",
        "white_words":"通达，没有过失，吉利的卜问。有所往则有利。",
        "picture":"雷风，恒。君子以立不易方。",
        "white_picture":"风雷荡涤，宇宙常新，这是恒卦的卦象。君子观此卦象，从而立于正道，坚守不易。"
    },
    "巽巽":{
        "name":"巽为风",
        "words":"小亨。利有攸往，利见大人。",
        "white_words":"稍见亨通。利于出行，利于会见王公贵族。",
        "picture":"随风，巽。君子以申命行事。",
        "white_picture":"长风相随，吹拂不断，是巽卦的卦象。君子观此卦象，取法于长吹不断的风，从而不断地申明教义，反复地颁行政令，灌输纲常大义。"
    },
    "坎巽":{
        "name":"水风井",
        "words":"改邑不改井，无丧无得。往来井井。汔至，亦未繘井，羸其瓶，凶。",
        "white_words":"改建邑落而不改建水井，等于什么也没有干。人们往来井边汲水，水井干涸淤塞，不去加以淘洗，反而将吊水罐打破，这是凶险之象。",
        "picture":"木上有水，井。君子以劳民劝相。",
        "white_picture":"水下浸而树木生长，这是井卦的卦象。君子观此卦象，取法于井水养人，从而鼓励人民勤劳而互相劝勉。"
    },
    "艮巽":{
        "name":"山风蛊",
        "words":"元亨，利涉大川。先甲三日，后甲三日。",
        "white_words":"大吉大利。利于涉水渡河，但须在甲前三日之辛日与甲后三日之丁日启程。",
        "picture":"山下有风，蛊。君子以振民育德。",
        "white_picture":"贤人如山居于上，宣布德教施于下，所谓山下有风，这是巽卦盼卦象。君子观此卦象，取法于吹拂万物的风，从而振救万民，施行德教。"
    },
    "坤巽":{
        "name":"地风升",
        "words":"元亨。用见大人，勿恤，南征吉。",
        "white_words":"非常亨通，有利于会见王公贵族，不用担忧。占得此爻，出征南方吉利。",
        "picture":"地中生木，升。君子以顺德，积小以高大。",
        "white_picture":"木植于地中，是升卦的卦象。君子观此卦象，从而遵循德义，加强修养，从细小起步，逐步培育崇高的品德。"
    },

    "乾坎":{
        "name":"天水讼",
        "words":"有孚，窒惕，中吉，终凶。利见大人，不利涉大川。",
        "white_words":"虽有利可图(获得俘虏)，但要警惕戒惧。其事中间吉利，后来凶险。占筮得此爻，有利于会见贵族王公，不利于涉水渡河。",
        "picture":"天与水违行，讼。君子以做事谋始。",
        "white_picture":"天水隔绝，流向相背，事理乖舛，这是讼卦的卦象。君子观此卦象，以杜绝争讼为意，从而在谋事之初必须慎之又慎。"
    },
    "兑坎":{
        "name":"泽水困",
        "words":"亨，贞，大人吉，无咎。有言不信。",
        "white_words":"通泰。卜问王公贵族之事吉利，没有灾难。筮遇此爻，有罪之人无法申辩清楚。",
        "picture":"泽无水，困。君子以致命遂志。",
        "white_picture":"水渗泽底，泽中干涸，是困卦的卦象。君子观此卦象，以处境艰难自励，穷且益坚，舍身捐命，以行其夙志。"
    },
    "离坎":{
        "name":"火水未济",
        "words":"亨，小狐汔济，濡其尾，无攸利",
        "white_words":"小狐狸快要渡过河，却打湿了尾巴。看来此行无所利。",
        "picture":"火在水上，未济。君子以慎辨物居方。",
        "white_picture":"火在水上，水不能克火，是未济卦的卦象。君子观此卦象，有感于水火错位不能相克，从而以谨慎的态度辨辩事物的性质，审视其方位。"
    },
    "震坎":{
        "name":"雷水解",
        "words":"利西南。无所往，其来复吉。有攸往，夙吉。",
        "white_words":"利于西南行，但是，若没有确定的目标，则不如返回，返回吉利。如果有确定的目标，则宜早行，早行吉利。",
        "picture":"雷雨作，解。君子以赦过宥罪。",
        "white_picture":"雷雨并作，化育万物，是解卦的卦象。君子观此卦象，从而赦免过失，宽宥罪人。"
    },
    "巽坎":{
        "name":"风水涣",
        "words":"亨，王假有庙。利涉大川，利贞。",
        "white_words":"亨通，因为君王亲临宗庙，禳灾祈福。利于涉水过江河。这是吉利的贞卜",
        "picture":"风行水上，涣。先王以享于帝，立庙。",
        "white_picture":"风行水上，是涣卦的卦象。先王观此卦象，从而享祭天帝，建立宗庙，推行尊天孝祖的“德教”"
    },
    "坎坎":{
        "name":"坎为水",
        "words":"习坎，有孚，维心亨，行有尚。",
        "white_words":"抓获俘虏，劝慰安抚他们，通泰。途中将得到帮助。",
        "picture":"水洊至，习坎。君子以常德行，习教事。",
        "white_picture":"坎为永，水长流不滞，是坎卦的卦象。君子观此卦象，从而尊尚德行，取法于细水长流之象，学习教化人民的方法。"
    },
    "艮坎":{
        "name":"山水蒙",
        "words":"亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
        "white_words":"通泰。不是我有求于幼稚愚昧的人，而是幼稚愚昧的人有求于我。第一次占筮，神灵告诉了他。轻慢不敬的再三占筮，轻慢不敬的占筮，神灵就不会告诉他。但还是吉利的卜问。",
        "picture":"山下出泉，蒙。君子以果行育德。",
        "white_picture":"山下有泉，泉水喷涌而出，这是蒙卦的卦象。君子观此卦象，取法于一往无前的山泉，从而以果敢坚毅的行动来培养自身的品德。"
    },
    "坤坎":{
        "name":"地水师",
        "words":"贞，丈人吉，无咎。",
        "white_words":"占问总指挥的军情，没有灾祸。",
        "picture":"地中有水，师。君子以容民畜众。",
        "white_picture":"“地中有水”，这是师卦的卦象。君子观此卦象，取法于容纳江河的大地，收容和畜养大众。"
    },

    "乾艮":{
        "name":"天山遁",
        "words":"亨。小利贞",
        "white_words":"通达。小有利之占问。",
        "picture":"天下有山，遁。君子以远小人，不恶而严。",
        "white_picture":"天下有山，天高山远，是遁卦的卦象。君子观此卦象，从而不用以恶报恶的方法对付小人，而是采取严厉的态度，挂冠悬笏，自甘退隐，远离小人。"
    },
    "兑艮":{
        "name":"泽山咸",
        "words":"亨，利贞。取女吉。",
        "white_words":"通达，吉利的贞卜。娶女，吉利。",
        "picture":"山上有泽，咸。君子以虚受人。",
        "white_picture":"山中有泽，山气水息，互相感应，是咸卦的卦象。君子观此卦象，取法于深邃的山谷，深广的大泽，从而虚怀若谷，以谦虚的态度，接受他人的教益。"
    },
    "离艮":{
        "name":"火山旅",
        "words":"小亨，旅贞吉。",
        "white_words":"稍见亨通。贞卜旅行，吉利。",
        "picture":"山上有火，旅。君子以明慎用刑，而不留狱。",
        "white_picture":"山上有火，洞照幽隐，这是旅卦的卦象。君子观此卦象，从而明察刑狱，慎重判决，既不敢滥施刑罚，也不敢延宕滞留。"
    },
    "震艮":{
        "name":"雷山小过",
        "words":"亨，利贞。可小事，不可大事。飞鸟遗之音。不宜上，宜下，大吉。",
        "white_words":"亨通，这是吉利的贞卜。但是只适宜于小事，不适宜大事。飞鸟空中过，叫声耳边留，警惕人们：登高必遇险，下行则吉利。",
        "picture":"山上有雷，小过。君子以行过乎恭，丧过乎衰，用过乎俭。",
        "white_picture":"山上有雷，是小过的卦象。君子观此卦象，惧畏天雷，不敢有过失。因而行事不敢过于恭谦，居丧不敢过度哀伤，用度不敢过于节俭，唯适中而已。"
    },
    "巽艮":{
        "name":"风山渐",
        "words":"利西南，不利东北。利见大人，贞吉。",
        "white_words":"筮遇此卦，利西南行，不利东北行。利见贵族王公，获吉祥之兆。",
        "picture":"山上有水，蹇。君子以反身修德。",
        "white_picture":"山石磷峋，水流曲折，是蹇卦的卦象。君子观此卦象，悟行道之不易，从而反求诸己，修养德行。"
    },
    "艮艮":{
        "name":"艮为山",
        "words":"艮其背，不获其身。行其庭，不见其人。无咎。",
        "white_words":"卸掉责任，挂笏隐退，朝列之中已看不到他的身影，在他的庭院中寻找，也没有找到。其人远走高飞，自无灾祸。",
        "picture":"兼山，艮。君子以思不出其位。",
        "white_picture":"两艮卦相重，艮为山，可见艮卦的卦象是高山重立，渊深稳重。君子观此卦象，以此为戒，谋不踰位，明哲保身。"
    },
    "坤艮":{
        "name":"地山谦",
        "words":"亨，君子有终。",
        "white_words":"通泰。筮遇此卦，君子将有所成就。",
        "picture":"地中有山，谦。君子以裒多益寡，称物平施。",
        "white_picture":"地中有山，内高外卑，居高不傲，这是谦卦的卦象。君子观此卦象，以谦让为怀，裁取多余昀，增益缺乏的，衡量财物的多寡而公平施予。"
    },

    "乾坤":{
        "name":"天地否",
        "words":"否之匪人。不利君子贞。大往小来。",
        "white_words":"为小人所隔阂，这是不利于君子的占卜，事业也将由盛转衰。",
        "picture":"天地不交，否。君子以俭德辟难，不可荣以禄。",
        "white_picture":"天地隔阂不能交感，万物咽窒不能畅釜，这是否卦的卦象。君子观此卦象，从而在国家政治否塞之时，应思隐居不仕，以崇尚俭约来躲避灾难，不要以利禄为荣。"
    },
    "兑泽":{
        "name":"泽地萃",
        "words":"亨，王假有庙。利见大人，亨，利贞。用大牲吉。利有攸往。",
        "white_words":"通泰。王到宗庙举行祭祀。占得此卦，利于会见贵族王公，亨通，这是吉利的贞兆。用牛牲祭祀，也很吉利，并且出行吉利。",
        "picture":"泽上于地，萃。君子以除戎器，戒不虞。",
        "white_picture":"泽水淹地，是萃卦的卦象。君子观此卦象，以洪水横流，祸乱丛聚为戒，从而修治兵器，戒备意外的变乱。"
    },
    "离坤":{
        "name":"火地晋",
        "words":"康侯用锡马蕃庶，昼日三接。",
        "white_words":"康侯用成王赐予的良马来繁殖马匹，一天多次配种。",
        "picture":"明出地上，晋。君子以自昭明德。",
        "white_picture":"太阳照大地，万物沐光辉”，是晋卦的卦象。君子观此卦象，从而光大自身的光明之德。"
    },
    "震坤":{
        "name":"雷地豫",
        "words":"利建侯行师。",
        "white_words":"有利于封侯建国，出兵打仗。",
        "picture":"雷出地奋，豫。先王以作乐崇德，殷荐之上帝，以配祖考。",
        "white_picture":"春雷轰鸣，大地震动，催发万物，这是豫卦的卦象。先王观此卦象，取法于声满大地的雷鸣，制作音乐，歌功颂德，光荣归于上帝，光荣归于祖考。"
    },
    "巽坤":{
        "name":"风地观",
        "words":"盥而不荐，有孚顒若。",
        "white_words":"祭祀时灌酒降神而不献人牲，因为用作祭祀的俘虏的头部肿了，不能用作祭品。",
        "picture":"风行地上，观。先王以省方，观民设教",
        "white_picture":"风行大地吹拂万物，这是观的卦象。先王观此卦象取法于周流八方的风，从而巡视邦国，观察民情，推行教化。"
    },
    "坎坤":{
        "name":"水地比",
        "words":"吉。原筮，元永贞，无咎。不宁方来，后夫凶。",
        "white_words":"吉利。同时再卜筮，仍然大吉大利。卜问长时期的吉凶，也没有灾祸。不愿臣服的邦国来朝，迟迟不来者有难。",
        "picture":"地上有水，比。先王以建万国，亲诸侯。",
        "white_picture":"地上有水，这是比卦的卦象。先王观此卦象，取法于水附大地，地纳江河之象，封建万国，亲近诸侯。"
    },
    "艮坤":{
        "name":"山地剥",
        "words":"不利有攸往。",
        "white_words":"有所往则不利。",
        "picture":"山附于地，剥。上以厚下，安宅。",
        "white_picture":"山在地上，风雨剥蚀，这是剥卦的卦象。君子观此卦象，以山石剥落，岩角崩塌为戒，从而厚结民心，使人民安居乐业。"
    },
    "坤坤":{
        "name":"坤为地",
        "words":"元，亨，利牝马之贞。君子有攸往，先迷后得主。利西南得朋，东北丧朋。安贞，吉。",
        "white_words":"大吉大利。占问雌马得到吉兆。君子前去旅行，先迷失路途，后来找到主人，吉利。西南行获得财物，东北行丧失财物。占问定居，得到吉兆。",
        "picture":"地势坤，君子以厚德载物。。",
        "white_picture":"大地的形势平铺舒展，顺承天道。君子观此卦象，取法于地，以深厚的德行来承担重大的责任。"
    }
}
fake_delay = 10
send_str = ""

# # 读取别卦数据
# def init_gua_data(json_path):
#     with open(gua_data_path, 'r', encoding='utf8') as fp:
#         global gua_data_map
#         gua_data_map = json.load(fp)


# 爻图标映射
yao_icon_map = {
    0: "- -",
    1: "---"
}

# 经卦名
base_gua_name_map = {
    0: "坤", 1: "震", 2: "坎", 3: "兑", 4: "艮", 5: "离", 6: "巽", 7: "乾"
}


# 数字转化为二进制数组
def base_gua_to_yao(gua, yao_length=3):
    result = []
    while gua >= 1:
        level = 0 if gua % 2 == 0 else 1
        gua //= 2
        result.append(level)
    while len(result) < yao_length:
        result.append(0)
    return result


# 二进制数组转化为数字
def base_yao_to_gua(array):
    array = array[:]
    while len(array) > 0 and array[-1] == 0:
        array.pop()
    result = 0
    for i in range(len(array)):
        if array[i] == 0:
            continue
        result += pow(2, i)

    return result


# 打印一个挂
def print_gua(gua):
    yao_list = base_gua_to_yao(gua, 6)
    up_yao_list = yao_list[0:3]
    up = base_yao_to_gua(up_yao_list)

    print_now(yao_icon_map[up_yao_list[2]])
    print_now(yao_icon_map[up_yao_list[1]] + " " + base_gua_name_map[up])
    print_now(yao_icon_map[up_yao_list[0]])

    print_now("")

    down_yao_list = yao_list[3:6]
    down = base_yao_to_gua(down_yao_list)
    print_now(yao_icon_map[down_yao_list[2]])
    print_now(yao_icon_map[down_yao_list[1]] + " " + base_gua_name_map[down])
    print_now(yao_icon_map[down_yao_list[0]])


# 使用梅花易数
def calculate_with_plum_flower():
    global send_str  # 如果send_str是全局变量
    # 起上卦
    print_now(f"使用梅花易数♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️")
    send_str += f"使用梅花易数♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️♣️\n\n"
    print_a_wait_animation("卜上卦：", fake_delay)
    up_base_gua = int(round(time.time() * 1000)) % 8
    up_yao_array = base_gua_to_yao(up_base_gua)
    print_now(f"上卦获取成功,上卦为:{base_gua_name_map[up_base_gua]}")
    send_str += f"上卦获取成功,上卦为:{base_gua_name_map[up_base_gua]}\n\n"
    # 起下卦
    print_a_wait_animation("正在获取下卦：", fake_delay)
    down_base_gua = random.randint(0, 999999999999) % 8
    down_yao_array = base_gua_to_yao(down_base_gua)
    print_now(f"上卦获取成功,下卦为:{base_gua_name_map[down_base_gua]}")
    send_str += f"上卦获取成功,下卦为:{base_gua_name_map[down_base_gua]}\n"
    # 组成卦象
    print_a_wait_animation("正在组成本卦：", fake_delay)
    print_now(f"------------------------------------------------本卦------------------------------------------------")
    send_str += f"------------------------------------------------本卦------------------------------------------------\n\n"
    yao_list = up_yao_array + down_yao_array
    gua = base_yao_to_gua(yao_list)
    print_gua(gua)
    # 读取本卦象信息
    gua_code = str(base_gua_name_map[up_base_gua]) + str(base_gua_name_map[down_base_gua])
    try:
        gua_data = gua_data_map[gua_code]
        print_now(f"本卦为:{gua_data['name']}")
        send_str += f"本卦为:{gua_data['name']}\n"
        print_now(f"辞:{gua_data['words']} 译:{ gua_data['white_words']}")
        send_str += f"辞:{gua_data['words']} 译:{ gua_data['white_words']}\n"
        print_now(f"象:{gua_data['picture']} 译:{gua_data['white_picture']}")
        send_str += f"象:{gua_data['picture']} 译:{gua_data['white_picture']}\n"
    except Exception as e:
        print_now(f"未找到卦象：{gua_code} 解读")
        send_str += f"未找到卦象：{gua_code} 解读"
    print_a_wait_animation("正在组成互卦：", fake_delay)
    print_now(f"------------------------------------------------互卦------------------------------------------------")
    send_str += f"------------------------------------------------互卦------------------------------------------------\n\n"
    # 读取互卦象信息
    up_hu_yao_list = [yao_list[4], yao_list[5], yao_list[0]]
    up_hu_gua = base_yao_to_gua(up_hu_yao_list)
    down_hu_yao_list = [yao_list[5], yao_list[0], yao_list[1]]
    down_hu_gua = base_yao_to_gua(down_hu_yao_list)
    hu_yao_list = up_hu_yao_list + down_hu_yao_list
    hu_gua = base_yao_to_gua(hu_yao_list)
    hu_gua_code = str(base_gua_name_map[up_hu_gua]) + str(base_gua_name_map[down_hu_gua])
    hu_gua_data = gua_data_map[hu_gua_code]
    print_gua(hu_gua)
    print_now(f"互卦为:{hu_gua_data['name']}")
    send_str += f"互卦为:{hu_gua_data['name']}\n"
    print_now(f"辞:{hu_gua_data['words']} 译:{hu_gua_data['white_words']}")
    send_str += f"辞:{hu_gua_data['words']} 译:{hu_gua_data['white_words']}\n"
    print_now(f"象:{hu_gua_data['picture']} 译:{hu_gua_data['white_picture']}")
    send_str += f"象:{hu_gua_data['picture']} 译:{hu_gua_data['white_picture']}\n"
    print_a_wait_animation("正在组成变卦：", fake_delay)
    print_now(f"------------------------------------------------变卦------------------------------------------------")
    send_str += f"------------------------------------------------变卦------------------------------------------------\n\n"
    change_index = int(round(time.time() * 1000)) % 6
    change_yao_list = yao_list[:]
    change_yao_list[change_index] = 0 if change_yao_list[change_index] == 1 else 1
    up_change_yao_list = change_yao_list[0:3]
    up_change_gua = base_yao_to_gua(up_change_yao_list)
    down_change_yao_list = change_yao_list[3:5]
    down_change_gua = base_yao_to_gua(down_change_yao_list)

    change_gua = base_yao_to_gua(change_yao_list)
    print_gua(change_gua)
    change_gua_code = str(base_gua_name_map[up_change_gua]) + str(base_gua_name_map[down_change_gua])
    change_gua_data = gua_data_map[change_gua_code]
    print_now(f"变卦为:{change_gua_data['name']}")
    send_str += f"变卦为:{change_gua_data['name']}\n"
    print_now(f"辞:{change_gua_data['words']} 译:{change_gua_data['white_words']}")
    send_str += f"辞:{change_gua_data['words']} 译:{change_gua_data['white_words']}\n\n"
    print_now(f"象:{change_gua_data['picture']} 译:{change_gua_data['white_picture']}")
    send_str += f"象:{change_gua_data['picture']} 译:{change_gua_data['white_picture']}\n\n"


def print_a_wait_animation(tips, times):
    global send_str  # 如果send_str是全局变量
    # animation = "|/-\\"
    animation = "😜🤪😍😘🥰😂🤣😇🤩🥳"
    idx = 0
    print(f"{tips}")
    send_str += f"{tips}"
    for i in range(times):
        if i == 0:
            print(f"占卜中：{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}---->>>",end="\r"),
            send_str += f"占卜中：{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}---->>>"
        elif i == times-1:
            print(f"{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}\n",end="\r"),
            send_str += f"{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}\n"
        else:
            print(f"{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}---->>>",end="\r"),
            send_str += f"{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}{animation[idx % len(animation)]}---->>>"
        idx += 1
        time.sleep(0.1)
    




# init_gua_data(gua_data_path)
calculate_with_plum_flower()
try:
    from notify import send
    if send_str != "":
        send("简易算命",f"{send_str}")
except Exception as e:
    print("检测到还未安装notify通知脚本") 