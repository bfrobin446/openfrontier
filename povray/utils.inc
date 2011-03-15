
#macro shell(obj, factor)
    difference {
        object { obj }
        object { obj
            scale factor
        }
    }
#end

#macro lrmirror(obj)
    union {
        object { obj }
        object { obj scale <-1, 1, 1> }
    }
#end
