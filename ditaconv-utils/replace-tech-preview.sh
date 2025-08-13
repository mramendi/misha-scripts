sed -i '/^include::\.\/technology-preview\.adoc\[\]$/c\
{FeatureName} is a Technology Preview feature only.\
\
{techpreview-snippet}
' $1
