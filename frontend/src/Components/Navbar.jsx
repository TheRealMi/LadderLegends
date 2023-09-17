import{Link} from 'react-router-dom'
function Navbar(){
    return (
         
        <nav class="headerNav">
            <a href="/" class="site-title">Ladder League</a>
            <ul>
               <CustomLink href='/Leaderboard'>Leaderboard</CustomLink>
               <CustomLink href='/Signup'>Sign up</CustomLink>

            </ul>

        </nav>
    

    )

}

function CustomLink({href, children, ...props }){
    return(
        <li>
            <a href={href}>{children}</a>
        </li>
    )
}
export default Navbar;