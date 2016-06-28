import re

test_string="""
 On September 14, 2015, the Laser Interferometer Gravitational-wave Observatory (LIGO) detected a gravitational-wave transient (GW150914); we characterize the properties of the source and its parameters. The data around the time of the event were analyzed coherently across the LIGO network using a suite of accurate waveform models that describe gravitational waves from a compact binary system in general relativity. GW150914 was produced by a nearly equal mass binary black hole of $36^{+5}_{-4} M_\odot$ and $29^{+4}_{-4} M_\odot$; for each parameter we report the median value and the range of the 90% credible interval. The dimensionless spin magnitude of the more massive black hole is bound to be $<0.7$ (at 90% probability). The luminosity distance to the source is $410^{+160}_{-180}$ Mpc, corresponding to a redshift $0.09^{+0.03}_{-0.04}$ assuming standard cosmology. The source location is constrained to an annulus section of $610$ deg$^2$, primarily in the southern hemisphere. The binary merges into a black hole of $62^{+4}_{-4} M_\odot$ and spin $0.67^{+0.05}_{-0.07}$. This black hole is significantly more massive than any other inferred from electromagnetic observations in the stellar-mass regime. 
"""
#expressions = re.findall(r"\$(.*)\$", )

def parse_dictionary(file):
    myvars = {}
    with open(file) as myfile:
        for line in myfile:
            name, var = line.partition(":")[::2]
            var.replace("\n", "")
            myvars[name.strip()] = var
    return myvars
            
def multiple_replace(dict, text):
  # Create a regular expression  from the dictionary keys
    multiples = re.findall(r"\$(.*)\$",  text)
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    ret = []
    # For each match, look-up corresponding value in dictionary
    for text in multiples:
        ret.append(regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) )
    return ret
#astro_replace = {
#     "M_{\\odot}": "suns",
#     "R_{\\odot}": "suns"
#     }

astro_replace = parse_dictionary("latex-thesaurus.txt")
#print astro_replace

print multiple_replace(astro_replace, test_string)
