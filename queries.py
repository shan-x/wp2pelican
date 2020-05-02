#!/usr/bin/python3
# coding: utf-8


get_posts = """
query GET_POSTS($first: Int, $after: String) {
    posts(first: $first, after: $after) {
        pageInfo {
            hasNextPage
            endCursor
        }
        edges {
            node {
                title
                date
                modified
                slug
                content
                categories {
                    nodes {
                        name
                    }
                }
                tags {
                    nodes {
                        name
                    }
                }
            }
        }
    }
}
"""

get_pages = """
query GET_PAGES($first: Int, $after: String) {
    pages(first: $first, after: $after) {
        pageInfo {
            hasNextPage
            endCursor
        }
        edges {
            node {
                title
                date
                modified
                slug
                content
            }
        }
    }
}
"""

get_menu_id = """
{ menus {
    nodes {
      name
      id
    }
  }
}
"""

get_menu = """
query GET_MENU($id: ID!) {
  menu(id: $id) {
    name
    slug
    menuItems {
      nodes {
          label
          url
          childItems {
            nodes {
              label
              url
            }
          }
      }
    }
  }
}
"""