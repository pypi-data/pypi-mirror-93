/*
 * pyramid-helpers -- Helpers to develop Pyramid applications
 * By: Cyril Lacoux <clacoux@easter-eggs.com>
 *     Valéry Febvre <vfebvre@easter-eggs.com>
 *
 * Copyright (C) 2011-2021 Cyril Lacoux, Easter-eggs
 * https://gitlab.com/yack/pyramid-helpers
 *
 * This file is part of pyramid-helpers.
 *
 * pyramid-helpers is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * pyramid-helpers is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


function partialLinkSetup() {
    $('a.partial-link').css({'outline': 'none'}).click(function(event) {
        var url = $(this).attr('href');
        var target = $(this).parents('div.partial-block:first');
        var partialKey = target.data('partial-key');
        var data = {};

        data[partialKey] = true;

        target.addClass('loading');
        target.load(url, data, function() {
            target.removeClass('loading');
            partialLinkSetup();
        });
        return false;
    });
}

/*
 * Initialization
 */
$(document).ready(function() {
    /* Handle «partial» links */
    partialLinkSetup();
});
