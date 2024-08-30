Taxonomy of Emotions
Inspired by the psychology of a market cycle (Hens and
Meier 2015), we design our emotion taxonomy. In con-
trast to existing emotion classes that consolidate positive
feelings into ”joy”, it attempts to classify diversified mood
proxies including hope, optimism, belief, and thrill. In or-
der to maximise the impact of the dataset, we link our tax-
onomy with existing studies in psychology that serve Ek-
man’s 6-emotions (Ekman 1992) (e.g. joy, surprise, dis-
gust, fear, anger, and sadness) and Plutchik’s 8-emotions
(Plutchik 1980). Examining an emotion taxonomy in behav-
ioral finance and psychology returns discrete emotions, but
some are too similar. To address this, we make a subset of
the data and ask two financial experts to annotate it with a
predefined set of emotions. We notice that too similar labels
such as hope, wish, desire, and confidence makes the anno-
tation task more difficult thus, similar items are combined
into a single representative emotion label (e.g. optimism).



Grouping Emotions
For mapping Ekman’s 6 emotions, we use a similar approach
to GoEmotions (Demszky et al. 2020)’ mapping. Also, we
use Plutchik’s 8 emotions to group our taxonomy as follows:
To reduce noise, the ambiguous label is discarded. Map-
ping to Plutchik’s emotions in StockEmotion.
• Grouping Ekman’s 6 emotions: anger (maps to: anger),
disgust (maps to: disgust), fear (maps to: anxiety, panic),
joy (amusement, belief, excitement, optimism), sadness
(maps to: depression) and surprise (all ambiguous emo-
tions).
• Grouping Plutchik’s 8 emotions: anticipation (map to:
optimism, confusion), anger (maps to: anger), disgust
(maps to: disgust), fear (maps to: anxiety, panic), joy
(amusement, excitement), sadness (maps to: depression),
surprise (surprise, ambiguous), and trust (maps to: be-
lief)
