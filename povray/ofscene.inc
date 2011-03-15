global_settings {
    assumed_gamma 1.0
    max_trace_level 256
    radiosity {
        /* defaults */
    }
}

#default {
    finish {
        ambient 0.0
    }
}

light_source {
    <1,10,-1> * 150, rgb <0.9, 0.9, 0.9>
    parallel
    point_at <0,0,0>
    rotate -y * OF_Heading
}

camera {
    perspective
    location vnormalize(<0,1,-0.7>) * OF_CameraRadius
    right x * 1
    up y * 1
    look_at <0,0,0>
    angle OF_CameraAngle
    rotate -y * OF_Heading
}
