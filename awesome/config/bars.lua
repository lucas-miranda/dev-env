local gears = gears
local awful = awful

-- select main screen
local main_screen = screen.primary

-- Wallpaper
--set_wallpaper(s)

-- tags
awful.tag({ "1", "2", "3", "4", "5" }, main_screen, awful.layout.layouts[1])

-- Bar Widgets
-----------------------

-- prompt
main_screen.prompt = awful.widget.prompt()

-- layout box
main_screen.layoutbox = awful.widget.layoutbox(s)
main_screen.layoutbox:buttons(gears.table.join(
    awful.button({ }, 1, function () awful.layout.inc( 1) end),
    awful.button({ }, 3, function () awful.layout.inc(-1) end),
    awful.button({ }, 4, function () awful.layout.inc( 1) end),
    awful.button({ }, 5, function () awful.layout.inc(-1) end)
))

-- text clock
textclock = wibox.widget.textclock()

-- taglist buttons
local taglist_buttons = gears.table.join(
    awful.button(
        { }, mouse_id.button_left, 
        function(t) 
            t:view_only() 
        end
    ),
    awful.button( 
        { }, mouse_id.button_right, 
        awful.tag.viewtoggle
    ),
    awful.button(
        { super_key }, mouse_id.button_right, 
        function(t)
            if client.focus then
                client.focus:toggle_tag(t)
            end
        end
    ),
    awful.button(
        { }, mouse_id.scroll_up, 
        function(t) 
            awful.tag.viewnext(t.screen) 
        end
    ),
    awful.button(
        { }, mouse_id.scroll_down, 
        function(t) 
            awful.tag.viewprev(t.screen) 
        end
    )
)

local tasklist_buttons = gears.table.join(
    awful.button(
        { }, 
        4, 
        function ()
            awful.client.focus.byidx(1)
        end
    ),
    awful.button(
        { }, 
        5, 
        function ()
            awful.client.focus.byidx(-1)
        end
    )
)

-- taglist
main_screen.taglist = awful.widget.taglist {
    screen  = main_screen,
    filter  = awful.widget.taglist.filter.all,
    buttons = taglist_buttons
}

-- tasklist
main_screen.tasklist = awful.widget.tasklist {
    screen  = main_screen,
    filter  = awful.widget.tasklist.filter.currenttags,
    buttons = tasklist_buttons
}

-- Create the wibox
main_screen.wibar = awful.wibar({ position = "top", screen = main_screen })

-- Add widgets to the wibox
main_screen.wibar:setup {
    layout = wibox.layout.align.horizontal,

    -- left widgets
    {
        layout = wibox.layout.fixed.horizontal,
        main_screen.taglist,
        main_screen.prompt
    },

    -- riddle widget
    main_screen.tasklist,

    -- right widgets
    {
        layout = wibox.layout.fixed.horizontal,
        wibox.widget.systray(),
        textclock,
        main_screen.layoutbox
    }
}

-- Key Bindings
-----------------------

for i, tag in ipairs(main_screen.tags) do
    key = tag.name

    if tonumber(key) ~= nil then
        key = "#" .. tonumber(tag.name) + 9
    end

    globalkeys = gears.table.join(
        globalkeys,

        -- switch to tag
        awful.key(
            { super_key }, key,
            function ()
                tag:view_only()
            end,
            { description = "view tag #"..i, group = "tag" }
        ),

        -- toggle tag display
        awful.key(
            { super_key, control_key }, key,
            function ()
                awful.tag.viewtoggle(tag)
            end,
            { description = "toggle tag #" .. i, group = "tag" }
        ),

        -- Move client to tag.
        awful.key(
            { super_key, shift_key }, key,
            function ()
                if client.focus then
                    client.focus:move_to_tag(tag)
                end
            end,
            { description = "move focused client to tag #"..i, group = "tag" }
        ),

        -- Toggle tag on focused client.
        awful.key(
            { super_key, control_key, shift_key }, key,
            function ()
                if client.focus then
                    client.focus:toggle_tag(tag)
                end
            end,
            { description = "toggle focused client on tag #" .. i, group = "tag" }
        )
    )
end
