from django.urls import reverse


def sidebar_links(request):
    sidebar_data = [
        {
            'url': reverse('accounts:profile'),
            'svg': """<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-user-circle"
                               width="24"
                               height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"
                               stroke-linecap="round" stroke-linejoin="round">
                               <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                               <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                               <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0"></path>
                               <path d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855"></path>
                          </svg>""",
            'title': 'Profile',
        },
        {
            'url': reverse('notes:note_list'),
            'svg': """<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-list-tree"
                                 width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                                 fill="none" stroke-linecap="round" stroke-linejoin="round">
                               <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                               <path d="M9 6h11"></path>
                               <path d="M12 12h8"></path>
                               <path d="M15 18h5"></path>
                               <path d="M5 6v.01"></path>
                               <path d="M8 12v.01"></path>
                               <path d="M11 18v.01"></path>
                            </svg>""",
            'title': 'Notes',
        },
        {
            'url': reverse('notes:note_create'),
            'svg': """<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-pencil-plus"
                                     width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                                     fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                    <path d="M4 20h4l10.5 -10.5a2.828 2.828 0 1 0 -4 -4l-10.5 10.5v4"></path>
                                    <path d="M13.5 6.5l4 4"></path>
                                    <path d="M16 19h6"></path>
                                    <path d="M19 16v6"></path>
                                </svg>""",
            'title': 'Add Notes',
        },
    ]

    return {'sidebar_data': sidebar_data}
