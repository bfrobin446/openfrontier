#include "math.inc"
#include "glass.inc"
#include "metals.inc"
#include "golds.inc"

#include "ofscene.inc"
#include "utils.inc"

#declare pigHull = pigment {
    rgb <0.5, 0.5, 0.55>
}
#declare texPanels = 
texture {
    pigment {
        pigHull
    }
    finish {
        specular 0.5
        roughness 0.01
        irid { 0.5 }
    }
    normal {
        bumps bump_size 0.3 scale 0.8
    }
}
texture {
    pigment {
        bozo
        color_map {
            [ 0.2 rgbt<0.1,0.1,0.1,0.7> ]
            [ 0.5 rgbt<0.1,0.1,0.1,1.0> ]
        }
        warp {
            turbulence 1
        }
        scale <0.4, 0.4, 1>
    }
}

#declare texGrime = texture {
    pigment {
        bozo
        color_map {
            [0.2 rgbt<0.1,0.05,0.05,0.1>]
            [0.5 rgbt<0.1,0.05,0.05,1>]
        }
        warp {
            turbulence 1
        }
    }
}


#declare texCannon =
texture {
    T_Chrome_1B
    normal {
        facets size 0.5
    }
}
texture {
    texGrime
    scale <0.1,0.1,0.4>
}


#ifndef (fSFoilOpenAngle)
    #declare fSFoilOpenAngle = 0;
#end

#local texFwdHull =
texture { texPanels }
texture {
    pigment {
        object {
            object {
                plane { x, 0 }
            }
            pigment {
                image_map {
                    png "noseart.png"
                    once
                }
            },
            pigment { rgbt<0,0,0,1> }
        }
    }
    rotate y * 90
    scale <1, 0.9, 1.8>
    translate <0,-0.6, 2.9>
}


difference { /* forward fuselage */
    sphere {
        <0,0,0>, 1
        scale <0.75, 1, 4>

    }
    cylinder { <1,-0.25,-2>, <-1,-0.25,-2>, 2 }
    plane { z, -2 }

    texture {
        object {
            intersection {
                box {
                    <-1, 0.33, 4>,<1, 1.1, 0.3>
                }
                plane {
                    <0,-0.4, 0.9>, 3.2
                }
            }
            texture { texFwdHull },

            texture { 
                object {
                    intersection {
                        box {
                            <-1, 0.35, 4>,<1, 1.1, 0.32>
                        }
                        plane {
                            <0,-0.4, 0.9>, 3.18
                        }
                    }
                    texture {
                        pigment { rgb 0.03 }
                    }
                    texture {
                        pigment { P_Gold1 }
                        finish { F_Glass6 }
                    }
                }
            }
        }
    }
    interior { I_Glass3 }
}

difference { /* engine housing */
    object {
        shell(
            intersection {
                sphere {
                    <0,0,0>, 1
                    scale <1.25,1.05,4>
                }
                box {
                    <-1.1,-1.05,-4>,<1.1,1.04,4>
                }
            }
            , 0.95
        )
        translate y * 0.05
    }
    plane {-z, 0}
    plane {z, -2.5}

    texture { texPanels }
}

#local fPulse = function {
    pattern {
        gradient z
        scallop_wave
        frequency 2
    }
}

#if (OF_Impulse)
    cone {
        <0, 0, -2.25>, 0.7, <0,0,-10>, 0.2
        hollow on
        pigment { rgbt<0,0,0,1> }
        interior {
            media {
                emission rgb<0, 0.5, 0.9>
                density {
                    function {
                        0.8 * pow(1 - fPulse(x, y, z), 2) * (1 - (pow(x, 2) + pow(y, 2)) * 2) + 0.2
                    }
                }
                density {
                    function { (z + 10) / 8 }
                }
            }
        }
        scale <1.25, 1.05, 1>
        translate y * 0.05
    }
#end

#declare fMainWingDihedral = -5;
#declare fMainWingSpan = 4.5;

#macro OnMainWing(obj)
    lrmirror(
        object {
            obj
            rotate z * fMainWingDihedral
        }
    )
#end

OnMainWing(
    prism {
        linear_spline
        linear_sweep
        -0.025, 0.025, 13,
        <0.75, 0.625>,
        <1.625, 0.5>,<2, 0>
        <fMainWingSpan, 0.75>, <fMainWingSpan, -0.0>,
        <2, -1.5>, <1.625,-3>,
        <1.25, -2.9>, <1.25, -1>
        <(1.1/cosd(fMainWingDihedral)), -1>, <(1.1/cosd(fMainWingDihedral)), 0.2>, <0.75, 0.2>, <0.75, 0.625>
        texture { texPanels }
    }
)

#declare fSFoilOriginX = 3;
#declare vSFoilRest = <1.1, 0.75>;
#declare fSFoilBaseAngle = acosd(
    vdot(
        vnormalize(
            vSFoilRest
            - vrotate(fSFoilOriginX * x, z * fMainWingDihedral)
        ),
        vnormalize(-vrotate(fSFoilOriginX * x, z * fMainWingDihedral))
    )
);

#declare fSFoilHingeRadius = 0.1;

lrmirror(
    intersection {
        box {
            <1.1, 1.2 * sind(fMainWingDihedral), -0.1>, <1.2, vSFoilRest.y, -1.4>
        }
        plane {
            y, 0
            rotate -z * (fSFoilBaseAngle - fMainWingDihedral)
            translate vSFoilRest
        }
        pigment { pigHull }
    }
)

#if (1)
    OnMainWing(
        prism {
            linear_spline
            linear_sweep
            -0.025, 0.025, 7,
            <-fSFoilHingeRadius,0.75>,<-fSFoilHingeRadius,-1.25>,
            <-2, -5>, <-2.5, -5>, <-3, -2>, <-3, 0.1>, 
            <-fSFoilHingeRadius, 0.75>

            rotate -z * (fSFoilBaseAngle + fSFoilOpenAngle)
            translate x * fSFoilOriginX
            texture { texPanels }
        }
    )
#end

OnMainWing(
    union {
        cylinder {
            <fSFoilOriginX, 0, 0.75>, <fSFoilOriginX, 0, -1.25>, fSFoilHingeRadius
        }
        cone {
            <fSFoilOriginX, 0, 0.75>, fSFoilHingeRadius, <fSFoilOriginX, 0, 0.75 + fSFoilHingeRadius>, fSFoilHingeRadius / 2
        }
        cone {<fSFoilOriginX, 0, -1.25>, fSFoilHingeRadius, <fSFoilOriginX, 0, -1.25 - fSFoilHingeRadius>, fSFoilHingeRadius / 2
        }
        texture {
            pigment { pigHull }
            finish { F_MetalC }
        }
    }
)

#macro OnSFoil(obj)
    OnMainWing(
        object {
            obj
            translate -x * fSFoilOriginX
            rotate -z * (fSFoilBaseAngle + fSFoilOpenAngle)
            translate x * fSFoilOriginX
        }
    )
#end

OnSFoil(
    union {
        cylinder {
            <0.5, 0.08, 2>, <0.5, 0.08, -1>, 0.05
            texture { texCannon }
        }
        intersection {
            shell (
                union {
                    cone { <0,0,0>, 0.12, <0,0,0.25>, 0.05 }
                    cone { <0,0,0>, 0.12, <0,0,-0.2>, 0.07 }
                }
                ,0.95
            )
            plane { z, 0.2 }
            translate <0.5, 0.08, 2.1>
            texture { texCannon }
        }
        prism {
            linear_spline
            linear_sweep
            -0.15, 0.15, 5,
            <0, 0>, <0.12, -0.4>, <0.12, -1.25>, <0, -1.75>, <0,0>
            rotate z * 90
            texture {
                pigment {
                    object {
                        object {
                            box { <-0.125, -0.1, -0.45>, <0.12, 0.15, -2> }
                        }
                        pigment { pigHull },
                        pigment {
                            gradient x
                            pigment_map {
                                [0.45 pigHull ]
                                [0.55 rgb 0.1 ]
                            }
                            triangle_wave
                            scale <0.05, 1, 1>
                        }
                    }
                }
            }
            texture {
                texGrime
                scale <0.15, 0.15, 0.5>
            }
            translate <0.5, 0.025, 0>
        }
    }
)
